# Iteration

**What went wrong:** In the first full run (skill + MCP server, fresh headless Sonnet session), the skill loaded and the `project_status` tool was available, but the agent never called the tool. It collected its own evidence with `git`, `find` and Read. It also broke the skill's output format: row #4 was marked "Partially met", but the skill only allows Met, Not met or Can't tell.

**Diagnosis:** SKILL.md never mentions `project_status`. Loading a skill doesn't make the agent use a tool, so the agent fell back on the tools it already knew. The off-format verdict suggests the three-verdict rule isn't stated firmly enough to stop the model from inventing a middle option. TODO (me): confirm or revise this diagnosis in my own words.

**What I changed and the result:** TODO (me): not done yet. Planned fix: tell SKILL.md to call `project_status` first when it's available, and say explicitly that partial progress counts as "Not met" (and to note what's missing). Then rerun the same prompt in a fresh session. Record whether `project_status` was called and whether every verdict was Met, Not met or Can't tell.
