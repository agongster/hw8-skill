# Iteration

## What went wrong

I built an MCP tool, `project_status`, so the checker would have a quick, reliable snapshot of the project. In the first real run, the agent loaded my skill and the tool was connected, but it never called it. It used `git`, `find` and Read instead, 22 times. It also gave one requirement "Partially met", which isn't one of the three verdicts my skill allows.

## Why

My SKILL.md never mentioned the tool. I had assumed that if the tool was available, the agent would use it. It didn't, because nothing told it to, so it used the tools it already knew. The "Partially met" problem was the same kind of thing: I listed three verdicts but never said "only these three", so the model made up a middle option.

## The fix

I added two things to SKILL.md:

1. "Start by calling the `project_status` tool" as the first step of checking, plus what to do if the tool isn't there.
2. "There is no Partially met." If anything is missing, the verdict is Not met, and the evidence says what's done and what isn't.

## Result

On the rerun, the agent called `project_status`, and every verdict was one of the three allowed ones.

The first call did fail once, though. My skill said to pass "the project's absolute path", and the agent guessed the argument was called `project_path`. The tool actually takes `project_folder`, so it got an error and retried. I changed the line to name `project_folder` explicitly and ran it again. This time the first call was correct.

## A smaller bug, found by unit tests

I also wrote 19 unit tests for the tool. One of them failed: if a project contains a broken symlink (a shortcut whose target was deleted), the whole tool crashed instead of returning a report. The file listing didn't handle that case. I made it list the file as "BROKEN LINK or unreadable" and keep going. Now all 19 tests pass.
