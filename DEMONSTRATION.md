# Demonstration

## The task

I used `progress-check` on this assignment itself. I asked it: "check my progress against the assignment requirements in README.md". My README is still half-finished, with TODOs in it, so I already knew roughly what the right answer was, which makes it easy to check whether the checker is right.

Every run was a fresh, headless Claude Code session using Sonnet. It could read files, run read-only `git`/`find`/`ls`, and call my `project_status` tool. It could not edit anything.

## Run 1: before the fix

The skill loaded on its own, and the MCP server was connected. But the agent never used my tool. It went straight to Bash and Read:

```
Skill progress-check
Read README.md
Bash  git status && ls -la && find .claude ...
Read  SKILL.md, DEMONSTRATION.md, ITERATION.md
Bash  find mcp -type f && cat .mcp.json
...   (22 tool calls, none of them project_status)

| 2 | MCP tool description | Not met (and stale) | README.md:13 says "not built yet", but it is built |
Checked 9 requirements: 2 met, 6 not met, 1 can't tell.
```

The first time I ran it, it also gave one row a "Partially met" verdict, which my skill doesn't allow. I didn't save that run, so the transcript above is from a rerun on Nov 6 with the same skill. That rerun had the same tool problem.

## Run 2: after the fix

After I changed SKILL.md (see ITERATION.md), the agent called `project_status` before anything else:

```
Skill progress-check
Read README.md
project_status {"project_folder": ".../hw8-skill"}
  -> Files (10) ... Git ... TODO / FIXME markers ...
Read  DEMONSTRATION.md, ITERATION.md, SKILL.md, prompt_log.md, .mcp.json
Bash  git log --oneline -3 && git diff --stat

| 3  | "What the MCP tool does" | Not met | README.md:13 still reads "TODO (not built yet...)" |
| 11 | Skill calls the MCP tool | Met     | SKILL.md:18 ... and in this session I called it first |
Checked 16 requirements: 7 met, 7 not met, 2 can't tell.
```

Every verdict was Met, Not met or Can't tell.

## What the checker caught

Both runs found the same real problems in my README. Line 13 still says the MCP tool is "not built yet", even though it is. Four sections are still TODOs: triggers, MCP install, "Confirmed to work in", and "Borrowed or adapted". Run 1 also caught that my ITERATION.md described a fix I hadn't actually made yet, which was true at the time.

Some things the checker got wrong or was unsure about:

- **It couldn't verify my unit tests.** It wasn't allowed to run Python, so it counted the 19 tests but couldn't confirm they pass. That's fair. In Run 2, though, it marked this "Not met", when its own rules say unverified should be "Can't tell".
- **Its summary line was wrong.** Run 2's table has 8 Met, 7 Not met and 1 Can't tell, but its last line says 7, 7 and 2.
- **The runs split the work up differently.** Run 1 checked 9 requirements and Run 2 checked 16, so the totals can't be compared, even though the README findings match.
- **"Never edits" is untested.** Neither run had Edit permission, so it couldn't have edited anything even if it tried.

## Do I agree?

I do agree with the checker's verdicts. 
