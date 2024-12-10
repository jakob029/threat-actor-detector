#!/bin/bash

# Check if .env folder exist
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  echo "Creating .env ..."
  python3 -m venv ../.env

  echo "Installing requirements ..."
  ../.env/bin/pip install -r ../requirements.txt

  if [ ! -f ../src/api/.env ]; then 
    echo "Creating src/api/.env ..."
    touch ../src/api/.env 
    echo "
# LLM options
TAD_LLM_MODEL=llama3.1                    # Model to use
TAD_LLM_ADDRESS=http://100.77.88.10       # Ollama address
TAD_LLM_PREPROPT_PATH=./src/api/prepromt  # Preprompt path

# Database options
TAD_MYSQL_HOST=100.77.88.30  	  # MySQL host
TAD_MYSQL_PASSWORD=<PASSWORD>   # User password
TAD_MYSQL_DATABASE=tad      	  # Database name
TAD_MYSQL_USER=<USER>          	# User name

API_ADDRESS=10.40.0.40

# Vector database options
VECTOR_DB_HOST=100.77.88.70     # Vector database host address
VECTOR_DB_PORT=5000             # Vector database host open port
    " >> ../src/api/.env

    if command -v vim 2>&1 >/dev/null; then
      echo "Opening vim ..."
      vim ../src/api/.env
    else
      echo "Lmao, nano pleb."
      nano ../src/api/.env
    fi
  else
    echo "src/api/.env already exists."
  fi

  echo "Build package ..."
  ../.env/bin/pip install -e ../

elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
  echo "Detected windows. -_-"
fi
