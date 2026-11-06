# hw8-skill

## What the skill does and when it triggers

This is a documentation skill that helps me document my process and AI actions. It is a checker: it reviews where a project stands against its own spec, README, or assignment requirements, and gives me a clean, easy-to-read report of what is met, what is not, and the actions left to do, with a file or command output cited for each item. It only reports; it never edits anything. It also gives me templates of information for me to fill in about the vision for the project/assignment.

When there are multiple possible directions for the architecture and design of the project, the AI should lay these options out for me and let me choose which direction to go in, rather than choosing for me.

**Triggers:** I want it to run whenever I'm not sure where a project is at: when I ask where things stand, what's left to do, whether it's ready to submit, or to check my work against a SPEC.md or the assignment requirements. It shouldn't run when I'm asking for actual work, like "fix this bug" or "write the README". I can also force it with `/progress-check`.

## What the MCP tool does

One tool, `project_status(project_folder, baseline="")`. It reads a project folder and its git history and returns one plain-text snapshot:

- every file with its size, with empty files marked `EMPTY`;
- the git branch, the last 10 commits, uncommitted changes, and (if you give a `baseline` commit) the files changed since then;
- every `TODO` / `FIXME` marker with its file and line number.

It's read-only and never changes the project. The skill tells the agent to call it first, so every check starts from the same facts instead of whatever the agent decides to look at.

## The friction that motivated this

I found that in my own work in this class, I would be unsure of how much progress was being made at any given point, and would need to do a good deal of my own testing and investigation to determine next steps.

> ok move to the next phase of the game. what is to be implemented next?
> (Naevia, 2026-10-29, `Naevia/prompt_log.md:66`)

> of the multiplayer features what is currently implemented?
> (fishing-sim, 2026-09-29, `agongster.github.io/fishing-sim/prompt_log.md:228`)

> real quick--walk me through how everything works at a high level. how are the sprites made, how is the multiplayer implemented, what is being done where, etc.
> (fishing-sim, 2026-10-08, `agongster.github.io/fishing-sim/prompt_log.md:401`)

These show that I couldn't tell from the project myself what was finished and what was left, and needed better guidelines for understanding the project's implementation and progress.

## How to install

**Skill:** copy the `skill/` folder into a skills directory and rename it to the skill's name (it must contain `SKILL.md`; the skill's name is `progress-check`):
- one project only: `<project>/.claude/skills/<skill-name>/SKILL.md`
- all projects: `~/.claude/skills/<skill-name>/SKILL.md`

**MCP server:** it needs Python 3.10+ and the MCP Python SDK. First set up a virtual environment:

```
cd <ABSOLUTE PATH TO THIS REPO>/mcp
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then register it with Claude Code. Use `--scope project` for one project, or `--scope user` for all projects:

```
claude mcp add --scope project project-status -- <ABSOLUTE PATH TO THIS REPO>/mcp/.venv/bin/python <ABSOLUTE PATH TO THIS REPO>/mcp/project_status_server.py
```

With `--scope project`, this writes a `.mcp.json` like the one in this repo. With `--scope user`, it saves the server to your user settings instead. The paths in this repo's `.mcp.json` are for my machine, so change them to yours. The first time you start Claude Code, approve the `project-status` server when it asks (or in `/mcp`).

To run the server's unit tests: `cd mcp && .venv/bin/python -m unittest -v`.

## Confirmed to work in

- **Claude Code** (CLI, headless `claude -p`, with Sonnet): the skill loaded on its own from a plain-English prompt, and it called the `project_status` tool. See DEMONSTRATION.md.

I haven't tested it in Codex or in interactive Claude Code / the VS Code extension.

## Borrowed or adapted

- The MCP server uses the official MCP Python SDK (the `mcp` package on PyPI) for the server and for connecting over stdio.

Nothing else was borrowed. The skill and the server were written for this assignment, with AI help (see below).

## AI use on this assignment

I used AI to help me refine the skill and create the MCP server, as well as to organize my documentation for this assignment. See `prompt_log.md` for the prompts and which model and tool handled each one.
