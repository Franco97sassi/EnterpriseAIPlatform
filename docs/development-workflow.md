# Development Workflow

Every feature in the Enterprise AI Platform follows this workflow.

## 1. Plan

Define:

- Problem to solve
- Expected behavior
- Files that may need changes
- Acceptance criteria
- Tests required

## 2. Implement

Implement the smallest change necessary to satisfy the requirements.

Rules:

- Follow AGENTS.md
- Use type hints
- Keep API routes thin
- Keep business logic in services
- Avoid unnecessary dependencies

## 3. Test

Run the automated test suite:

pytest -v

All tests must pass before continuing.

## 4. Verify

Verify:

- Application starts correctly
- API behavior matches requirements
- Existing functionality still works
- No secrets are committed
- No unnecessary dependencies were introduced

## 5. Review

Review the implementation for:

- Correctness
- Readability
- Maintainability
- Security
- Test coverage

A feature is complete only after all five stages succeed.