# hw8-skill

## What the skill does and when it triggers

This is a documentation skill that helps me document my process and AI actions. It is a checker: it reviews where a project stands against its own spec, README, or assignment requirements, and gives me a clean, easy-to-read report of what is met, what is not, and the actions left to do, with a file or command output cited for each item. It only reports; it never edits anything. It also gives me templates of information for me to fill in about the vision for the project/assignment.

When there are multiple possible directions for the architecture and design of the project, the AI should lay these options out for me and let me choose which direction to go in, rather than choosing for me.

**Triggers:** TODO (write the situations in which you want it to run, the current `description` in `skill/SKILL.md` says it runs when I ask where a project stands, what is left to do, whether it is ready to submit, or to check progress against requirements. Rewrite this in my own words.)

## What the MCP tool does

TODO (not built yet: one tool, what it reaches, and what it returns.)

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

**MCP server:** TODO (the exact config to register it, with machine-specific paths marked, e.g. `<ABSOLUTE PATH TO THIS REPO>`.)

## Confirmed to work in

TODO (list only the tools I actually tested: Claude Code, Codex, ...)

## Borrowed or adapted

TODO (anything from outside, and where from. Write "nothing" if so.)

## AI use on this assignment

I used AI to help me refine the skill and create the MCP server, as well as to organize my documentation for this assignment. See `prompt_log.md` for the prompts and which model and tool handled each one.
