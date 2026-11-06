"""Unit tests for project_status. Run from mcp/: .venv/bin/python -m unittest -v

Every test builds its own throwaway folder (and git repo where needed), so the
real project is never touched.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from project_status_server import MAX_FILES, MAX_MARKERS, MAX_TEXT_BYTES, project_status

GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], env=GIT_ENV,
                          capture_output=True, text=True, check=True).stdout.strip()


def snapshot(root):
    return {p: p.read_bytes() for p in Path(root).rglob("*") if p.is_file()}


class ProjectStatusTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text=""):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def make_repo(self):
        git(self.root, "init", "-q", "-b", "main")
        self.write("README.md", "hello\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-q", "-m", "first")

    # --- bad input ---
    def test_missing_folder(self):
        self.assertEqual(project_status(str(self.root / "nope")), f"Not a folder: {self.root / 'nope'}")

    def test_file_instead_of_folder(self):
        path = self.write("a.txt", "x")
        self.assertTrue(project_status(str(path)).startswith("Not a folder:"))

    def test_tilde_is_expanded(self):
        old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(self.root)  # keep the walk inside the temp folder
        try:
            self.assertEqual(project_status("~").splitlines()[0], f"# Project status: {self.root}")
        finally:
            os.environ["HOME"] = old_home

    # --- files ---
    def test_empty_file_flagged_and_sizes_shown(self):
        self.write("ITERATION.md")
        self.write("README.md", "abc")
        out = project_status(str(self.root))
        self.assertIn("- ITERATION.md  (EMPTY)", out)
        self.assertIn("- README.md  (3 bytes)", out)
        self.assertIn("## Files (2)", out)

    def test_skip_dirs_ignored(self):
        self.write("src/main.py", "x")
        for d in (".venv", "node_modules", "__pycache__", ".godot"):
            self.write(f"{d}/junk.py", "# TODO hidden")
        out = project_status(str(self.root))
        self.assertIn("## Files (1)", out)
        self.assertNotIn("junk.py", out)

    def test_file_list_truncated(self):
        for i in range(MAX_FILES + 5):
            self.write(f"f{i:03}.txt", "x")
        out = project_status(str(self.root))
        self.assertIn(f"## Files ({MAX_FILES + 5})", out)
        self.assertIn("- ... 5 more not shown", out)

    def test_broken_symlink_does_not_crash(self):
        self.write("real.txt", "x")
        os.symlink(self.root / "gone.txt", self.root / "dangling.txt")
        out = project_status(str(self.root))
        self.assertIn("- dangling.txt  (BROKEN LINK or unreadable)", out)
        self.assertIn("- real.txt  (1 bytes)", out)

    # --- git ---
    def test_not_a_repo(self):
        self.write("a.txt", "x")
        self.assertIn("Not a git repository.", project_status(str(self.root)))

    def test_clean_repo(self):
        self.make_repo()
        out = project_status(str(self.root))
        self.assertIn("Branch: main", out)
        self.assertRegex(out, r"Recent commits:\n[0-9a-f]+ \d{4}-\d\d-\d\d first")
        self.assertIn("(clean)", out)

    def test_status_keeps_leading_space(self):
        # The bug found in manual testing: " M README.md" lost its leading space.
        self.make_repo()
        self.write("README.md", "changed\n")
        self.write("new.txt", "x")
        out = project_status(str(self.root))
        self.assertIn("Uncommitted changes (git status --short):\n M README.md\n?? new.txt", out)

    def test_baseline_diff(self):
        self.make_repo()
        base = git(self.root, "rev-parse", "HEAD")
        self.write("added.py", "x\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-q", "-m", "second")
        out = project_status(str(self.root), baseline=base)
        self.assertIn(f"Changed since {base} (git diff --stat):", out)
        self.assertIn("added.py", out)

    def test_baseline_no_changes(self):
        self.make_repo()
        self.assertIn("(no changes)", project_status(str(self.root), baseline="HEAD"))

    def test_bad_baseline_reported_not_raised(self):
        self.make_repo()
        self.assertIn("(git failed:", project_status(str(self.root), baseline="no-such-ref"))

    # --- markers ---
    def test_markers_with_line_numbers(self):
        self.write("a.py", "ok\n# TODO: finish\nx = 1  # FIXME later\n")
        out = project_status(str(self.root))
        self.assertIn("- a.py:2: # TODO: finish", out)
        self.assertIn("- a.py:3: x = 1  # FIXME later", out)

    def test_marker_word_boundary_and_case(self):
        self.write("a.md", "TODOS list\ntodo lowercase\nMYTODO\n")
        self.assertTrue(project_status(str(self.root)).endswith("## TODO / FIXME markers\n(none)"))

    def test_marker_line_cut_to_140_chars(self):
        self.write("a.py", "# TODO " + "x" * 300)
        line = next(l for l in project_status(str(self.root)).splitlines() if l.startswith("- a.py:1:"))
        self.assertEqual(len(line), len("- a.py:1: ") + 140)

    def test_marker_list_truncated(self):
        self.write("a.py", "# TODO\n" * (MAX_MARKERS + 3))
        self.assertIn("- ... 3 more not shown", project_status(str(self.root)))

    def test_binary_and_large_files_skipped(self):
        (self.root / "img.bin").write_bytes(b"\xff\xfe TODO \x00\x81")
        self.write("big.txt", "# TODO big\n" + "x" * MAX_TEXT_BYTES)
        out = project_status(str(self.root))
        self.assertNotIn("img.bin:", out)
        self.assertNotIn("big.txt:", out)
        self.assertIn("img.bin", out)  # still listed as a file

    # --- read-only ---
    def test_does_not_modify_project(self):
        self.make_repo()
        self.write("README.md", "changed # TODO\n")
        before, status_before = snapshot(self.root), git(self.root, "status", "--short")
        project_status(str(self.root), baseline="HEAD")
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(git(self.root, "status", "--short"), status_before)


if __name__ == "__main__":
    unittest.main()
