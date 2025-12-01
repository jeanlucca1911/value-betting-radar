#!/bin/bash
echo "Starting application..."
echo "PORT is $PORT"
uvicorn main:app --host 0.0.0.0 --port $PORT
