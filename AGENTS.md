# Enterprise AI Platform - Agent Instructions

## Project

Enterprise AI Platform is a Python project designed to demonstrate
end-to-end AI Engineering practices.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Pytest

## Development Rules

1. Follow clean and modular Python architecture.
2. Use type hints for functions and methods.
3. Keep API routes thin and move business logic to services.
4. Validate API inputs and outputs with Pydantic.
5. Never hardcode secrets or API keys.
6. Add or update tests when implementing functionality.
7. Do not introduce dependencies unless they are necessary.
8. Keep functions small and focused on one responsibility.

## Verification

Before considering a task complete:

1. Run the automated tests.
2. Verify that the application starts successfully.
3. Check that existing functionality still works.
4. Document important architectural decisions.