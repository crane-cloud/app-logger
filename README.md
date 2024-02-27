# Application logger

Logging application and user actions.

### Project Setup

Follow these steps to have a local running copy of the app.

### Clone The Repo

```bash
git clone https://github.com/crane-cloud/app-logger.git
```

### Running application with Docker

---
`make` is a build automation tool that is used to manage the build process of a software project.

- In the project directory, running `make` shows you a list of commands to use.
- Run `make start` to start the application and required services.
- Run `make connect-to-container` to connect to the FastAPI application container.

### Available services

---

- `app-logger`: Application API server (Default port: 8000)
- `logger-celery-worker`: Celery worker for background tasks
- `logger-mongo-db`: Applications MongoDB Server (Default port: 27001)
- `logger-flower`: Celery flower Dashboard (Default port: 5555)
- `logger-redis-db`: Redis Database Server (Default port: 6380)
