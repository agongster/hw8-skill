# Demonstration

**Task I used it on:** I pointed `progress-check` at this repo (hw8-skill) and asked it to check my progress against the assignment requirements in README.md. The `project_status` MCP server was registered in `.mcp.json`. A fresh headless Claude Code session (Sonnet) ran the check with the prompt "check my progress against the assignment requirements in README.md". Before that, I tested the tool by itself: on this repo with baseline `c424ae4` it listed the right files, flagged ITERATION.md as EMPTY, and showed the commits, diff and TODOs. On `/nonexistent` it returned "Not a folder" without crashing, and on restaurant-db it reported the right 4 files and git history.

**Run 1:** The server connected and the tool was available. The skill loaded on its own from the plain-English prompt. It ran `git`, `find` and Read itself and never called `project_status`. It returned 13 verdicts with file:line evidence, a "left to do" list, and one open decision with options. Row #4 used "Partially met", which isn't one of the skill's allowed verdicts.

> TODO (me): paste a trimmed excerpt of the run 1 transcript (the tool calls and a few verdict rows).

**Run 2:** TODO (me): not done yet. Rerun the same prompt in a fresh session (ideally after the ITERATION fix) and paste a trimmed transcript here.

**What the checker caught:** Its findings were accurate where I checked them. For example, it flagged README.md:13, which still said "not built yet", as stale. The "never edits" rule wasn't really tested: the run didn't have permission to edit, so it couldn't have edited even if it tried.

**Whether I agree with it:** TODO (me): go through the 13 verdicts and say which ones I agree with and why.
