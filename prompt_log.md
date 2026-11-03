# Prompt Log: hw8-skill

## Models & tools

- **Claude Code** (VS Code extension) is the tool for every prompt below. The model is noted per prompt, since I switched models partway through.
- Per-prompt model and tools are listed under each prompt.

## Prompts (verbatim)

### 1. 2026-11-03

**Model / tools:** Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code. Tools used: Bash (look at the folder and my old logs), Write (this file).

> I think I would like the skill to go in a different direction, let's start from scratch. i'm going to build a new repository called hw8-skill. please work in there. do not add anything until i tell you to, for now just help me with the ideation process and to understand what i am creating. log my prompts and summary of your response in prompt_log.md (which you can create in hw8-skill).

**Summary of response:** Claude created only this file and added nothing else to the repo. It explained what I'm building: a skill (instructions that change how the agent works) that must be a *checker*, plus an MCP server (one tool that gives the agent new reach). It then pitched new directions based on friction in my past logs:

1. **"Is it actually live?" deploy checker** + an MCP tool that fetches the deployed site or Render status. Evidence: fishing-sim prompts "i see the commit pushed to github but it's not updating on render", "i don't see the chat rooms?", "i do not see a chat button in the pushed version."
2. **"Prove it before you say it" claims checker** (are the agent's "done / stopped / tests pass" claims backed by command output?). Evidence: Naevia E, "Said the test backend was stopped when it wasn't", and H, "Wrote test expectations from assumptions instead of the data".
3. **Scope checker** ("what did the agent touch that I didn't ask for?") + an MCP tool that diffs a repo against a baseline commit. Evidence: Naevia A (lock-file dependencies removed unasked) and L (two of Ryan's SPEC lines changed).
4. **Spec / acceptance-criteria checker** + an MCP tool that runs the project's tests or game headlessly. Evidence: hw7-game SPEC and Naevia acceptance table.

It asked which friction felt most real to me, which client I plan to use (Claude Code or Codex), and what outside service I'd want the MCP tool to reach.

### 2. 2026-11-03

**Model / tools:** Claude Sonnet 5.5 (`claude-sonnet-5-5`) in Claude Code (I switched with `/model sonnet`). Tools used: Bash (read the repo, edit this log), Write (README and SKILL.md).

> please read through what I have in README: refine and organize it better, and create a very baseline skill for it. also in prompt_log, please note which models and tools are used for each prompt.

**Summary of response:** Claude reorganized my README into the headings the assignment asks for, keeping my wording, and put `TODO` markers where I haven't written anything yet (triggers, MCP tool, evidence quotes, MCP install config, confirmed tools, borrowed work). It wrote a baseline `skill/SKILL.md` named `progress-report`: report what's done / left / unknown, lay out options for design decisions instead of choosing, and give fill-in templates for the project vision. It added the per-prompt model and tools notes to this log. It also pointed out that this skill isn't yet a checker, which the assignment requires.

### 3. 2026-11-03

**Model / tools:** Claude Sonnet 5.5 (`claude-sonnet-5-5`) in Claude Code. Tools used: Write (SKILL.md), Bash (edit README and this log).

> sure, please make the skill a checker and update the README accordingly.

**Summary of response:** Claude rewrote `skill/SKILL.md` as `progress-check`: it finds a standard (named file, SPEC.md, pasted requirements, or README), splits it into requirements, gives each a verdict (Met / Not met / Can't tell) with cited evidence, then lists what's left, open decisions as options for me to choose, and fill-in templates for missing vision. It never edits files, and it treats the agent's own claims as something to verify. It updated the README's description of the skill to match and added the skill's name to the install section.

### 4. 2026-11-03

**Model / tools:** Claude Sonnet 5.5 (`claude-sonnet-5-5`) in Claude Code. Tools used: Bash (searched my past session transcripts with the earlier `get_my_prompts` script, and grepped my prompt logs for line numbers).

> can you find a short quote from my own prompt logs that demonstrates this friction? there should be something that is along the lines of "ok, now what comes next?"

**Summary of response:** Claude searched my real prompts across fishing-sim, restaurant-db, lyric-search, hw7-game and Naevia for "what's next / what's the status" questions and gave four candidates with log line numbers: Naevia "ok move to the next phase of the game. what is to be implemented next?", fishing-sim "of the multiplayer features what is currently implemented?", lyric-search "is it done?", and fishing-sim "real quick--walk me through how everything works at a high level...". It recommended pairing the Naevia and fishing-sim "currently implemented" quotes, and did not edit my README.

### 5. 2026-11-03

**Model / tools:** Claude Sonnet 5.5 (`claude-sonnet-5-5`) in Claude Code. Tools used: Edit (README), Bash (this log).

> can you log all three prompts? i think in combination they all demonstrate different key points

**Summary of response:** Claude read "all three" as the Naevia "what is to be implemented next?" prompt and the two fishing-sim prompts ("currently implemented?" and "walk me through how everything works"), and put them in the README's friction section with their sources. It left "is it done?" out, left a `TODO` for me to explain in my own words what each one shows, and logged prompts 4 and 5 here.

### 6. 2026-11-03

**Model / tools:** Claude Sonnet 5.5 (`claude-sonnet-5-5`) in Claude Code. Tools used: Bash (this log). No other tools; this was ideation only.

> what should the corresponding mcp server do?

**Summary of response:** Claude said the MCP tool should give the `progress-check` skill evidence it can't easily get on its own. It offered three candidates: (A) a `project_status` snapshot of the repo (which required files exist or are empty, commits and uncommitted changes since a baseline, TODO markers), (B) a "claims vs. actions" tool that reads session transcripts and shows what the agent said it finished next to what it actually ran, and (C) a live-site checker. It recommended A for the first version because it's the simplest to build and demo. It noted honestly that A is the weakest on "new reach", and that B is the most distinctive.

### 7. 2026-11-03

**Model / tools:** Claude Sonnet 5.5 (`claude-sonnet-5-5`) in Claude Code. Tools used: Bash (create venv, run tests, register the server, run a headless check), Write (`mcp/project_status_server.py`). A separate fresh Sonnet 5.5 session ran `progress-check` as the test.

> that makes sense, please implement A for my first version.

**Summary of response:** Claude built `mcp/project_status_server.py` (one tool, `project_status(project_folder, baseline)`: file list with EMPTY flags, git branch/commits/uncommitted changes/diff since a baseline, and TODO/FIXME markers with line numbers) plus `mcp/requirements.txt` (`mcp>=2.3,<3`) and a `.gitignore`. Testing found one bug (git's first status line lost its leading space), which it fixed. It then confirmed the tool works over real stdio, registered it in `.mcp.json`, and symlinked the skill into `.claude/skills/progress-check` to try it. In that end-to-end run the server connected and the skill triggered, but the checker never called `project_status`; it used Bash and Read instead. Claude did not change the skill and reported this to me as a finding.

### 8. 2026-11-03

**Model / tools:** Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code (I switched back with `/model opus`). Tools used: Bash (this log, and a check that hw7-game has a SPEC.md to suggest as a test target).

> Can you give me a very clear report on what you tested and the results of each? what kind of questions or prompts should make it call this tool/skill? how do i run it myself and what is something i can do to test the efficacy of this skill?

**Summary of response:** Claude gave a table of the 6 tests run so far and their results, including that the end-to-end run triggered the skill but never called `project_status`, and that the checker used a "Partially met" verdict the skill doesn't allow. It also listed what was never tested (Codex, interactive Claude Code, the "never edits" rule). It listed prompts that should and shouldn't trigger the skill, explained that triggering the skill is not the same as calling the tool, gave step-by-step commands to run it myself (interactive and headless), and suggested efficacy tests: a planted-problems test scored for what it caught and what it falsely flagged, a trigger test, a with/without-tool comparison, a consistency test, and a "never edits" test.
