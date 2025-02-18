#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting RAG application..."

# Activate virtual environment (if using one)
# source venv/bin/activate  # Uncomment if using a virtual environment

#Check if Ollama is installed, install if missing
if ! command -v ollama &> /dev/null
then
    echo "Ollama is not installed. Installing now..."
    curl -fsSl https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed"
fi

#Start Ollama in the background
ollama serve &

#Wait for Ollama to be ready
sleep 5

#Ensure Deepseek 1.5B model is available
if ! ollama list | greq -q "deepseek-r1:1.5b"; then
    echo "Deepseek 1.5B model not found. Pulling it now..."
    ollam pull deepseek-r1:1.5b
fi

# Install dependencies
pip install --no-cache-dir -r requirements.txt

#serve ollama 
ollama run 
OLLAMA_HOST=127.0.0.1:12000 ollama serve

# Start the server
uvicorn app:app --host 0.0.0.0 --port 8000
