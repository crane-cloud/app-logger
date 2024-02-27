# Application logger

Logging application and user actions.

## Project Setup

Follow these steps to have a local running copy of the app.

### Clone The Repo

```bash
git clone https://github.com/crane-cloud/app-logger.git
```

### Directly on your machine

---

#### Set-up MongoDB

Either use the mongo image `docker pull mongo:latest` or set-up a local instance or get a DB url link from atlas
After starting the DB and it's running,
Create a logs database

- `activity-logs` (for development)

#### Create a Virtual Environment

App was developed with Python 3.6.

Make sure you have `poetry` installed on your machine.

Create a virtual environment with `poetry shell`.

Install the dependencies:

```bash
poetry install
```

Create a `.env` file (which defines the environment variables used) at the root of the app.

Add the following details, customizing as needed:

```bash
export MONGO_URI=
```

Run the application:

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Running application with Docker

---

`make` is a build automation tool that is used to manage the build process of a software project.

- In the project directory, running `make` shows you a list of commands to use.
- Run `start-docker-services` to start the application and required services.
