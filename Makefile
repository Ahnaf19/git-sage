.PHONY: setup activate install lock remenv

# Setup full environment and install deps
setup:
	conda env create -f environment.yml

# Activate the conda environment
activate:
	conda activate gitsage

# Activate env and install using uv
install:
	uv pip install -r requirements.txt

# Lock current versions to lock file
lock:
	uv pip compile requirements.txt --output-file=requirements.lock.txt

# Remove the conda environment
remenv:
	conda env remove -n gitsage -y
