# Clean Architecture

Lately, for some reason, I am obsessed with software architecture. Probably because for the first time in my developer career, the products that I am building need to scale, be testable and developed by a team.

After some researching I am building this repo to test ideas and develop best practices for Python and Web projects.

## Example

This repo contains a TODO app example. It's objective is to test ideas on software architecture with Python. The app will be accessible via a web UI, API and CLI (for testing how to manage different entry points in the same codebase) and use two different database backends (again, to test how to manage this at the software architecture level).

### A bad example ?

You can find an implementation of such API in [bad_example.py](bad_example.py). You can start the API with the command

```
uvicorn bad_example:app
```

And you can interact with it via the interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

> Note: This implementation uses an in-memory database. Also, you'll need to install all the dependencies to make it work (which I deliberately will not mention).

As you can see, the same file contains the API routes, business logic and database access implementation. Is this bad? The answer is... it depends. If our objective is to demo an idea fast and we will be the only developer, it is a good solution, it serves its purpose. But, what if we want to test it to make sure there are no bugs? or add more features? or change the database? or develop it in a team? Then, it is a very bad solution. As a general rule:

- First, make it work
- Then, make it well
- Finally, make it efficient

### Backlog

- Users must be able to register with username and password
- Users must be able to login in order to use the protected user-level functionality
- Users must be able to create, retrieve, update and delete their TODOs.
- User must be able to interact with the library via a web API
- User must be able to interact with the library via a CLI
- User must be able to interact with the library via a web UI

### Roadmap

- v0: Core python library that allows for user registration and manage TODOs CRUD.
- v1: API
- v2: CLI
- v3: web UI

The system is testable at the following levels:

- unit tests (pytest) for use cases (fast, good for TDD)
- integration tests (pytest) for API, cli and databases (slow)
- end to end test (playwright for web ui) for use cases + API/CLI/UI with database (very slow, good for CI/CD)

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

## Git

The project is based on the following structure of branches:

- main: production code
- develop: development version to be merged to main
- features: multiple branches for individual features to be added on develop.

## References

https://www.youtube.com/watch?v=bieO6YOZ4uc
https://github.com/cosmicpython/book
https://leanpub.com/clean-architectures-in-python
