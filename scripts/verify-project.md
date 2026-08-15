# Skill: Verify Project

## Purpose

Verify that the Enterprise AI Platform is in a valid state after
a code change.

## When to Use

Use this skill after implementing or modifying functionality.

## Steps

1. Read the project rules in `AGENTS.md`.

2. Run:

   `python scripts/verify.py`

3. Confirm that all automated tests pass.

4. Confirm that the verification process exits successfully.

5. If verification fails:
   - Do not mark the task as complete.
   - Identify the failing test or validation.
   - Fix the underlying problem.
   - Run verification again.

## Success Criteria

The skill succeeds only when:

- All automated tests pass.
- The verification script completes successfully.
- Existing functionality remains operational.