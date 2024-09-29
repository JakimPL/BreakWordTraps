#!/bin/bash

if lsof -i :8000; then
    echo "Port 8000 is already in use. Trying to kill the process..." 
    lsof -ti :8000 | xargs kill -9
fi

echo "Running FastAPI app..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# --reload: automatyczne ponowne ładowanie aplikacji po zmianie plików
# --host: 0.0.0.0 umożliwia dostęp do aplikacji na lokalnej sieci
# --port: port, na którym działa aplikacja (domyślnie 8000)
