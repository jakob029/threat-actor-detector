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
### Linux (and WSL) or Mac OS
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
TAD_MYSQL_USER=api          	# User name
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
