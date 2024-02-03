#!/bin/bash

service rabbitmq-server start

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# Initialize rabbitmq
python3 starter.py

tail -f /dev/null
```