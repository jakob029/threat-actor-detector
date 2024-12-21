# General setup instructions

# Developer instructions

The Python code in this application shall be run using python version 3.10 or newer.
Older versions may result in package errors.

Clone the repository
```bash
git clone https://github.com/jakob029/threat-actor-detector.git
cd threat-actor-detector
```

## Set up Python environment
### Linux (and WSL) or Mac OS
```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv .env
source .env/bib/activate
pip install -r requirements.txt
```
### Windows
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Set up environment variables

### For API

#### Linux (and WSL) or Mac OS
First, create a file in the given to this path: ./threat-actor-detector/src/api/.env
```bash
touch threat-actor-detector/src/api/.env
```

Then, write the following to the file:
```bash
# LLM options
TAD_LLM_MODEL=llama3.1                    # Model to use
TAD_LLM_ADDRESS=http://100.77.88.10       # Ollama address
TAD_LLM_PREPROPT_PATH=./src/api/prepromt  # Preprompt path

# Database options
TAD_MYSQL_HOST=100.77.88.30  	# MySQL host
TAD_MYSQL_PASSWORD=<PASSWORD>   # User password
TAD_MYSQL_DATABASE=tad      	# Database name
TAD_MYSQL_USER=<USER>          	# User name
IOC_MYSQL_DATABASE=ioc_apt_mapping

API_ADDRESS=10.40.0.40

# Vector database options
VECTOR_DB_HOST=100.77.88.70     # Vector database host address
VECTOR_DB_PORT=5000             # Vector database host open port
```

### For vector database API

#### Linux (and WSL) or Mac OS

The following describes how to create a .env file for the vector database API.

First, create a file in the given to this path: threat-actor-detector/src/vector_db_api/.env

```bash
touch threat-actor-detector/src/vector_db_api/.env
```

Then, write the following to the file:
```bash
# Database options
TAD_MYSQL_HOST=100.77.88.30  	     # MySQL host
TAD_MYSQL_PASSWORD=<PASSWORD>        # User password
TAD_MYSQL_DATABASE=ioc_apt_mapping   # Database name
TAD_MYSQL_USER=<USER>          	     # User name

CHROMA_DB_ADDRESS=10.50.0.50
```

### For forntend
The following describes how to create a .env file for the vector database API.

First, create a file in the given to this path: threat-actor-detector/src/vector_db_api/.env

```bash
touch threat-actor-detector/src/frontend/.env
```

Then, write the following to the file:
```bash
FRONTED_KEY="<TOKEN>"
API_ADDR="<API_ADDRESS>"
FRONTEND_ADDR="<ADDRESS_TO_BIND>"
```

### Windows
Execute the following in the local environment:
```powershell
set TAD_LLM_MODEL=llama3.1
set TAD_LLM_ADDRESS=http://100.77.88.10
set TAD_LLM_PREPROPT_PATH=./src/api/prepromt

set TAD_MYSQL_HOST=100.77.88.30
set TAD_MYSQL_PASSWORD=<PASSWORD>
set TAD_MYSQL_DATABASE=tad
set TAD_MYSQL_USER=api
```

## Push code to github
Initially create a local branch:
```bash
git checkout -b <BRANCH_NAME>
```

Then, complete the code edits intended.

Make sure the cude edits pass the automated test by running:
```bash
tox
```

Then do the following for each edited file:
```bash
git add <FILE_PATH>
```

Make a local commit by running:
```bash
git commit -m "<COMMIT_MESSAGE>"
```

Finaly, push the commit to github:
```bash
git push --set-upstream origin <BRANCH_NAME>
```

Once this is complete, you can initale a pull requests on github.
This will initiate the process of pushing the code to the main branch,
utilizing automatic checks and code review to certify a satisfactory
result.

Once the code has been merged to the main branch, run:
```bash
git checkout main
git pull
```

To resync the local repository to the current main branch on github.
