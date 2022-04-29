# Clean Architecture

For some reason, lately I am obsessed with software architecture. Probably because for the first time in my developer careers, the products I am building need to scale, be testable and developed by a team.

After some researching I am building this repo to test ideas and develop best practices for Python and Web projects.

## Project structure

![relations](/pics/relations.png)

- src
  - Domain: entities, simple models with attributes (Pydantic)
  - Application: Use Cases, business logic
  - Interfaces: interfaces between use cases and external systems
  - tests
- api
- ui
- cli
- database

![flow](/pics/flow.png)

## Example

This repo contains a TODO app example with the following features:

- web ui (sveltekit app)
- web API (FastAPI)
- cli (Typer)
- core library (Python)
- local database (?)
- cloud database (firestore)

The system is testable at the following levels:

- unit tests (pytest) for use cases (fast, good for TDD)
- integration tests (pytest) for API, cli and databases (slow)
- end to end test (playwright for web ui) for use cases + API/CLI/UI with database (very slow, good for CI/CD)

## Git

The project is based on the following structure of branches:

- main: production code
- develop: development version to be merged to main
- features: multiple branches for individual features to be added on develop.

## References

https://www.youtube.com/watch?v=bieO6YOZ4uc
https://github.com/cosmicpython/book
https://leanpub.com/clean-architectures-in-python
