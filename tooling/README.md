## Docker

Docker is an open platform for developing, shipping, and running applications inside
lightweight, isolated environments called containers. Containers include everything the
app needs to run, so you don't have to worry about what's installed on the host machine.
Docker uses a client-server architecture where the client talks to a daemon that handles
building, running, and distributing containers.

---

## Kubernetes

Kubernetes is an open source platform for managing containerized workloads at scale.
It takes care of scaling, failover, and deployment patterns automatically — for example,
it restarts failed containers and replaces unhealthy ones without human intervention.
You describe the desired state of your app and Kubernetes continuously works to match it.

---

## GitLab

GitLab is a fully integrated DevSecOps platform built on top of Git. It covers the entire
software lifecycle in one place: source code management, CI/CD pipelines, security scanning,
and deployment tools. Unlike a patchwork of separate tools, everything lives in a single
data plane so teams always work from one source of truth.

---

## FastAPI

FastAPI is a modern, high-performance Python web framework for building APIs using standard
Python type hints. It automatically validates request data, serializes responses, and generates
interactive API documentation with zero extra setup. It is one of the fastest Python frameworks
available, on par with NodeJS and Go.

---

## SQLAlchemy

SQLAlchemy is the go-to database toolkit for Python, providing an ORM that lets you work with
database tables as plain Python classes instead of writing raw SQL. You declare table columns
as typed class attributes and SQLAlchemy handles the translation to SQL. It supports many
databases such as PostgreSQL, MySQL, and SQLite through interchangeable dialects.

---

## FastAPI with SQLAlchemy

FastAPI and SQLAlchemy are commonly paired together: SQLAlchemy handles database persistence
while FastAPI handles HTTP routing and validation. The standard pattern is to create a
SQLAlchemy session factory and inject a session into each request using FastAPI's Depends()
system. Pydantic models are kept separate from ORM models to cleanly split what the API sees
from what the database stores.

---

## Alembic

Alembic is a database migration tool built on top of SQLAlchemy. It tracks schema changes
such as adding tables or renaming columns as versioned Python scripts, each with an upgrade()
and downgrade() function. It can also auto-generate migration scripts by comparing your ORM
models to the actual database, saving a lot of manual work.

---

## Swagger UI

Swagger UI lets anyone visualize and interact with an API directly in the browser, automatically
generated from an OpenAPI Specification. Developers can fill in parameters and hit Execute to
test any endpoint without writing a single line of client code. FastAPI serves Swagger UI for
free at /docs the moment you start your server.

## Bugs in the follow-up exercises

1. `app/api/v1/endpoints/order/crud.py`  
   Function: `calculate_price`

2. `app/api/v1/endpoints/order/crud.py`  
   Function: `create_order`

3. `app/api/v1/endpoints/order/stock_logic/stock_beverage_crud.py`  
   Function: `beverage_is_available`

4. `app/api/v1/endpoints/order/stock_logic/stock_ingredients_crud.py`  
   Functions: `reduce_stock_of_ingredients` and `increase_stock_of_ingredients`