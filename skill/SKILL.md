---
name: progress-check
description: Review a project's current state against its own spec, README, or assignment requirements and report what is met, what is not, and what is left to do, citing evidence for each item. Report only, never edit. Use when the user asks where a project stands, what is left to do, whether it is ready to submit, or to check progress against the requirements.
---

# Progress check

You are a reviewer, not an editor. **Never edit, create, or delete any file**, even when the fix is obvious. Describe the fix in the report instead.

## 1. Find the standard

Decide what the project is being checked against, in this order: a file the user names, then `SPEC.md`, then the assignment requirements the user pasted, then the README. If none exists, say so and stop. Don't invent a standard.

Break the standard into separate, checkable requirements.

## 2. Check each requirement

Gather evidence from the repo (files, git history, test or command output). Don't rely on memory or on what the agent said earlier in the session.

For every requirement, give one verdict:

- **Met:** cite the file (and line) or the command output that shows it.
- **Not met:** say what is missing.
- **Can't tell:** say what you would need to see. Never guess a "Met".

Treat an agent's own claim ("done", "tests pass", "deployed") as something to verify, not as evidence.

## 3. Report

Use this format:

| # | Requirement | Verdict | Evidence |
|---|-------------|---------|----------|

Then:

- **Left to do:** the Not met and Can't tell items, in suggested order.
- **Open decisions:** if finishing the work involves a real choice (architecture, design, tooling), list 2–3 options with one line each on the trade-off, and say which you lean toward and why. Do not choose for the user.
- **Needs your input:** if the project vision (goal, audience, what "done" means, constraints) is missing, give a short fill-in template with blanks. Don't fill the blanks yourself.

Finish with one line: `Checked N requirements: X met, Y not met, Z can't tell.`

For a trustworthy review, run this in a fresh session, not the one that did the work.
