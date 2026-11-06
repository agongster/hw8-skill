"""MCP server with one tool: project_status.

Gives the progress-check skill the same facts every time: which files exist or
are empty, what git says has changed, and where TODO/FIXME markers are left.
It is read-only; it never writes to the project it inspects.
"""
import os
import re
import subprocess
from pathlib import Path

from mcp.server.mcpserver import MCPServer

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".godot", ".import"}
MARKER = re.compile(r"\b(TODO|FIXME)\b")
MAX_FILES, MAX_MARKERS, MAX_TEXT_BYTES = 200, 40, 500_000

mcp = MCPServer("project-status")


def _walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            yield Path(dirpath) / name


def _git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), "-c", "core.fsmonitor=false", *args],
        capture_output=True, text=True, timeout=20,
    )
    return result.stdout.strip("\n") if result.returncode == 0 else f"(git failed: {result.stderr.strip()})"


@mcp.tool()
def project_status(project_folder: str, baseline: str = "") -> str:
    """Return a factual snapshot of a project folder, for checking progress.

    Reports (1) every file with its size, marking files that are EMPTY,
    (2) git state: branch, recent commits, uncommitted changes, and, if
    `baseline` (a commit, tag, or branch) is given, the files changed since it,
    and (3) every TODO / FIXME marker with file and line number.
    `project_folder` is an absolute path. Nothing is modified.
    """
    root = Path(os.path.expanduser(project_folder)).resolve()
    if not root.is_dir():
        return f"Not a folder: {root}"

    files = list(_walk(root))
    out = [f"# Project status: {root}", f"\n## Files ({len(files)})"]
    for path in files[:MAX_FILES]:
        try:
            size = path.stat().st_size
        except OSError:  # e.g. a symlink whose target is gone
            out.append(f"- {path.relative_to(root)}  (BROKEN LINK or unreadable)")
            continue
        out.append(f"- {path.relative_to(root)}  ({'EMPTY' if size == 0 else f'{size} bytes'})")
    if len(files) > MAX_FILES:
        out.append(f"- ... {len(files) - MAX_FILES} more not shown")

    out.append("\n## Git")
    if not (root / ".git").exists():
        out.append("Not a git repository.")
    else:
        out.append(f"Branch: {_git(root, 'rev-parse', '--abbrev-ref', 'HEAD')}")
        out.append("Recent commits:\n" + (_git(root, "log", "-10", "--date=short", "--pretty=format:%h %ad %s") or "(none)"))
        out.append("Uncommitted changes (git status --short):\n" + (_git(root, "status", "--short") or "(clean)"))
        if baseline:
            out.append(f"Changed since {baseline} (git diff --stat):\n" + (_git(root, "diff", "--stat", baseline) or "(no changes)"))

    out.append("\n## TODO / FIXME markers")
    found = []
    for path in files:
        try:
            if path.stat().st_size > MAX_TEXT_BYTES:
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if MARKER.search(line):
                    found.append(f"- {path.relative_to(root)}:{number}: {line.strip()[:140]}")
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable
    out.extend(found[:MAX_MARKERS] or ["(none)"])
    if len(found) > MAX_MARKERS:
        out.append(f"- ... {len(found) - MAX_MARKERS} more not shown")
    return "\n".join(out)


if __name__ == "__main__":
    mcp.run()  # stdio
