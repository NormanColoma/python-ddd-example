# DDD and Hexagonal Architecture in Python

This repository was created with the proposal of using it as a boilerplate for creating DDD
applications in Python. This example presents a relatively simple problem, our focus will be 
on applying DDD principles in Python. In a real world scenario we would have a more complex business rules than that.

## Project explanation 
***

For this example we’re going to build a very simple application for managing football teams where we can:

* Create a new team
* Sign player
* Get team
* View historical transactions of each team (this implementation will be out of scope)

Let’s consider some restrictions and invariants within our domain:

* Each team and player must be identified and must have a name
* A team cannot hire more than eleven players

## How to run
***
### Requirements

* Docker
* Docker Compose

### Steps

1. Clone the repository
2. Run `docker-compose up` in the root folder. It will build the docker images (flask and mongo) and run them.
3. The application will be running on `http://localhost:3000`
