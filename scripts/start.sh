#!/usr/bin/env bash
#!/bin/bash


# Start the server
poetry run python uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4