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

### A better example

First, let's structure our project a little bit.

#### Backlog

List of high level features that we desire for our app:

- Users must be able to register with username and password
- Users must be able to login in order to use the protected user-level functionality
- Users must be able to create, retrieve, update and delete their TODOs.
- User must be able to interact with the library via a web API
- User must be able to interact with the library via a CLI
- User must be able to interact with the library via a web UI

#### Roadmap

Main features included in major releases:

- v0: Core python library that allows for user registration and manage TODOs CRUD.
- v1: API
- v2: CLI
- v3: web UI

#### Sprints

Each release will be developed following TDD principles and documented.

- v0
  - v0.1: user registration
  - v0.2: firebase users registration
  - v0.3: user login
  - v0.4: todos creation
  - v0.5: todos retrieval
  - v0.6: todos update
  - v0.7: todos delete
  - v0.8: firebase users backend
  - v0.9: firebase todos backend
- v1
  - v1.1: api user routes
  - v1.2: api todos routes
- v2
  - v2.1: cli user functions
  - v2.2: cli user functions
- v3
  - v3.1: ui user registration
  - v3.2: ui user login
  - v3.3: ui todos CRUD

## Project structure

- api
- cli
- src
  - application: Use Cases, business logic
  - docs: library documentation
  - domain: entities, simple models with attributes (Pydantic), errors
  - infrastructure: repositories
  - tests
- ui

![relations](/pics/relations.png)

![flow](/pics/flow.png)

## Git

The project is based on the following structure of branches:

- main: production code
- develop: development version to be merged to main
- features: multiple branches for individual features to be added on develop.

## Testing

The system is testable at the following levels:

- unit tests (pytest) for use cases (fast, good for TDD)
- integration tests (pytest) for API, cli and databases (slow)
- end to end test (playwright for web ui) for use cases + API/CLI/UI with database (very slow, good for CI/CD)

TDD rules:

1. Test first, code later
2. Add the bare minimum amount of code you need to pass the tests
3. You shouldn’t have more than one failing test at a time
4. Write code that passes the test. Then refactor it.
5. A test should fail the first time you run it. If it doesn’t ask yourself why you are adding it. 6. Never refactor without tests.

## Workflow

When a new feature is added, the following workflow is followed:

1. Create a new branch called `feature/<name_of_the_feature>`.
2. Implement tests
3. Implement minimum required code to pass the tests
4. Refactor
5. Document
6. Merge to develop if all tests pass and docs are up to date (solve conflicts)
7. Merge to main if all tests pass and docs are up to date

The same goes for when a bug is found.

## References

https://www.youtube.com/watch?v=bieO6YOZ4uc
https://github.com/cosmicpython/book
https://leanpub.com/clean-architectures-in-python
