# GitSage

GitSage is an open-source LLM-powered tool that explains and answers questions about any GitHub repository. Built using LangChain, Ollama, Tree-sitter, and ChromaDB, it lets developers query unfamiliar codebases like a personal AI mentor.

> [!NOTE]
> Being Developed with Python 3.12 and tested on macOS/Linux environments for Python 3.10-3.13. Some parts of the following are under development.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![LangChain](https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Ollama](https://img.shields.io/badge/ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![ChromaDB](https://img.shields.io/badge/chromadb-FF6B6B?style=for-the-badge&logo=database&logoColor=white)
![uv](https://img.shields.io/badge/uv-3C3C3C?style=for-the-badge&logo=uv&logoColor=white)
![Uvicorn](https://img.shields.io/badge/uvicorn-0E1E25?style=for-the-badge&logo=uvicorn&logoColor=white)
![Loguru](https://img.shields.io/badge/loguru-FF8700?style=for-the-badge&logo=loguru&logoColor=white)
![Apache 2.0 License](https://img.shields.io/badge/license-Apache%202.0-blue?style=for-the-badge)

[![CI](https://github.com/Ahnaf19/git-sage/actions/workflows/ci.yml/badge.svg)](https://github.com/Ahnaf19/git-sage/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Ahnaf19/git-sage/branch/main/graph/badge.svg)](https://codecov.io/gh/Ahnaf19/git-sage)
[![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://github.com/Ahnaf19/git-sage)
[![Code style: pre-commit](https://img.shields.io/badge/code%20style-pre--commit-brightgreen)](https://github.com/pre-commit/pre-commit)

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Project Phase Plan](#project-phase-plan)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running GitSage](#running-gitsage)
- [Sample Usage](#sample-usage)
- [Contributing](#contributing)
- [Learning Objectives](#learning-objectives)
- [License](#license)

## Overview

GitSage transforms how developers explore and understand codebases by combining the power of:

1. **Smart Code Parsing**: Uses Tree-sitter to intelligently chunk code while preserving semantic structure
2. **Vector Search**: Leverages ChromaDB for efficient similarity search across code embeddings
3. **Local LLM Integration**: Powered by Ollama for privacy-focused, offline code analysis
4. **Contextual Answers**: Provides detailed explanations with direct source code references

Perfect for onboarding to new projects, code reviews, architectural understanding, and learning from open-source repositories.

## Core Features

### Intelligent Code Analysis

- **Tree-sitter Integration**: Parses code with full syntax awareness
- **Language Support**: Python, JavaScript, TypeScript, Java, C++, and more
- **Semantic Chunking**: Preserves function and class boundaries

### AI-Powered Understanding

- **Local LLM Processing**: Privacy-focused analysis using Ollama
- **Context-Aware Responses**: Answers include relevant code snippets
- **Multiple Model Support**: Compatible with various Ollama models

### Vector Search & Retrieval

- **ChromaDB Integration**: Fast similarity search across code embeddings
- **Semantic Matching**: Finds relevant code based on intent, not just keywords
- **Efficient Storage**: Optimized vector storage and retrieval

### Repository Management

- **GitHub Integration**: Clone repositories or fetch via GitHub API
- **Flexible Repository Access**: Choose between git clone (full history) or API fetch (lightweight)
- **Incremental Updates**: Efficient processing of repository changes
- **Multi-Repository Support**: Analyze multiple codebases simultaneously

## Project Phase Plan

### Phase 1: Repository Ingestion [ON GOING!]

- [x] **Repository Fetching**: Downloads repositories via git clone or GitHub API
- [x] **File Discovery**: Identifies supported source code and config files
- [ ] **Language Detection**: Determines programming languages used and focus on files that way

> [!NOTE]
> Language Detection is skipped for future scope.

### Phase 2: Code Parsing & Chunking

- [ ] **Tree-sitter Parsing**: Generates Abstract Syntax Trees (AST) for each file
- [ ] **Semantic Chunking**: Splits code into meaningful units (functions, classes, modules)
- [ ] **Metadata Extraction**: Captures file paths, line numbers, and code structure

### Phase 3: Embedding Generation

- [ ] **Text Preprocessing**: Prepares code chunks for embedding
- [ ] **Vector Generation**: Creates embeddings using sentence transformers
- [ ] **ChromaDB Storage**: Stores vectors with metadata for efficient retrieval

### Phase 4: Query Processing

- [ ] **Query Embedding**: Converts user questions to vector representations
- [ ] **Similarity Search**: Finds most relevant code chunks using ChromaDB
- [ ] **Context Assembly**: Gathers relevant code snippets and metadata
- [ ] **LLM Generation**: Uses Ollama to generate comprehensive answers

## Project Structure

```
git-sage/
├── README.md                    # Project documentation
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment configuration template
├── config/
│   ├── __init__.py
│   ├── settings.py              # Application configuration
│   └── models.py                # Ollama model configurations
├── src/
│   ├── __init__.py
│   ├── git_sage/
│   │   ├── __init__.py
│   │   ├── main.py              # Main application entry point
│   │   ├── cli.py               # Command-line interface
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── repository.py    # GitHub repository handling
│   │       ├── parser.py        # Tree-sitter code parsing
│   │       ├── embeddings.py    # Vector embedding generation
│   │       ├── vectordb.py      # ChromaDB operations
│   │       └── llm.py           # Ollama LLM integration
├── data/
│   ├── repositories/            # Cloned repositories
│   ├── embeddings/              # ChromaDB vector storage
│   └── cache/                   # Temporary files and cache
├── tests/
│   ├── __init__.py
│   ├── test_parser.py           # Tree-sitter parsing tests
│   ├── test_embeddings.py       # Embedding generation tests
│   └── test_integration.py      # End-to-end tests
└── examples/
    ├── basic_usage.py           # Simple usage examples
    └── advanced_queries.py      # Complex query patterns
```

## Prerequisites

- **Python 3.8 or newer** (Python 3.12+ recommended)
- **Conda/Miniconda** (for environment management)
- **Git** (for repository cloning)
- **Make** (optional - for automated setup commands)
- **4GB+ RAM** (recommended for embedding generation)
- **2GB+ disk space** (for models and repository storage)

### Install Prerequisites

**Install Conda (if not already installed):**

```bash
# Download and install Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```

> [!WARNING]
> Installing Conda can be bypassed, but then makefile commands might not work properly.

**Install Make (optional - for automated setup):**

```bash
# Check if Make is installed
make --version

# Install Make if needed:
# macOS
brew install make

# Ubuntu/Debian
sudo apt-get install build-essential
```

## Setup Instructions

Choose one of the following setup methods:

### Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/Ahnaf19/git-sage.git
cd git-sage

# One-command setup using Makefile (requires Make & Conda)
make setup    # Creates the conda environment
conda activate gitsage # Activates conda env
make install  # Activates env and installs dependencies using uv
```

#### Makefile Commands Reference (Optional)

```bash
make setup     # Creates the conda environment from environment.yml
make activate  # Activates the conda environment
make install   # Installs dependencies using uv
make lock      # Creates requirements.lock.txt with locked versions
make remenv    # Removes the conda environment
make test      # Run tests (optional)
```

Pre-commit hooks setup & usage (optional):

```bash
pre-commit clean
pre-commit install # Sets up pre-commit hooks
pre-commit autoupdate
pre-commit migrate-config
pre-commit run --all-files # run pre-commit manually
```

### Manual Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ahnaf19/git-sage.git
cd git-sage
```

### 2. Create Conda Environment

```bash
# Step 1: Create the environment from environment.yml
conda env create -f environment.yml

# Step 2: Activate the environment
conda activate gitsage

# Step 3: Install Python libraries quickly using uv
uv pip install -r requirements.txt

# Step 4 (optional): Lock current dependency versions into a separate file
uv pip compile requirements.txt --output-file=requirements.lock.txt

# Set up pre-commit hooks
pre-commit install
```

## Running GitSage

### Method 0: Run current (tag 0.1.0) main entrypoint

```bash
# Basic usage with default settings
python main.py https://github.com/pallets/flask

# Use GitHub API instead of git clone
python main.py https://github.com/microsoft/vscode --mode api

# Custom target directory
python main.py https://github.com/user/repo --target-dir ./my-repos

# With GitHub token for private repos or higher rate limits
python main.py https://github.com/private/repo --token your_github_token

# SSH URLs also work
python main.py git@github.com:user/repo.git

# Get help
python main.py --help
```

> [!WARNING]
> Below methods and usages are yet to be implemented. Stay tuned!

### Method 1: Command Line Interface

```bash
# Analyze a repository (default: clone mode)
python -m git_sage.main analyze <repo-url>

# Analyze using GitHub API
python -m git_sage.main analyze <repo-url> --mode api

# Specify output directory
python -m git_sage.main analyze <repo-url> --target-dir ./output

# Provide GitHub token for private repos
python -m git_sage.main analyze <repo-url> --token <your_token>

# Query the codebase
python -m git_sage.main query "<your question>"

# Interactive Q&A session
python -m git_sage.main interactive

# Show help for all commands
python -m git_sage.main --help

# Show help for a specific command
python -m git_sage.main analyze --help

# Analyze a GitHub repository (clone method - default)
python -m git_sage analyze https://github.com/user/repository

# Analyze using GitHub API (faster, no git history)
python -m git_sage analyze https://github.com/user/repository --mode api

# Specify target directory for cloned repos
python -m git_sage analyze https://github.com/user/repository --target-dir ./my-repos

# Use GitHub token for private repos or higher rate limits
python -m git_sage analyze https://github.com/user/private-repo --token your_github_token

# Ask questions about the codebase
python -m git_sage query "How does authentication work in this project?"

# Interactive mode
python -m git_sage interactive
```

### Method 2: Python API

```python
from git_sage import GitSage

# Initialize GitSage
sage = GitSage()

# Analyze a repository using git clone (default)
sage.analyze_repository("https://github.com/user/repository")

# Analyze using GitHub API (faster for large repos)
sage.analyze_repository(
    "https://github.com/user/repository",
    mode="api",
    token="your_github_token"  # Optional for private repos
)

# Ask questions
response = sage.query("Explain the main application structure")
print(response.answer)
print("Sources:", response.sources)
```

### Method 3: Jupyter Notebook

```python
# In a Jupyter notebook
import sys
sys.path.append('/path/to/git-sage')

from git_sage import GitSage
sage = GitSage()

# Interactive analysis
sage.interactive_session()
```

## Sample Usage

### Basic Repository Analysis

```bash
$ python -m git_sage analyze https://github.com/fastapi/fastapi
Repository fetched successfully (clone mode)
Parsing 157 source files...
Generating embeddings...
Storing in vector database...
Analysis complete! Ready for queries.

# Using GitHub API for faster analysis
$ python -m git_sage analyze https://github.com/fastapi/fastapi --mode api
Repository fetched via GitHub API
Parsing 157 source files...
Generating embeddings...
Storing in vector database...
Analysis complete! Ready for queries.
```

### Interactive Querying

```bash
$ python -m git_sage query "How does FastAPI handle dependency injection?"

Searching codebase...
Found 5 relevant code sections

**Answer:**
FastAPI uses a sophisticated dependency injection system based on Python's type hints...

**Relevant Code:**
1. `fastapi/dependencies/utils.py:45-67` - Core dependency resolver
2. `fastapi/routing.py:123-145` - Route dependency handling
3. `docs_src/dependencies/tutorial001.py:1-15` - Basic usage example

Would you like me to explain any specific part in more detail?
```

### Advanced Analysis

```python
# Analyze multiple repositories with different methods
sage = GitSage()
repos = [
    {"url": "https://github.com/fastapi/fastapi", "mode": "clone"},
    {"url": "https://github.com/tiangolo/full-stack-fastapi-postgresql", "mode": "api"}
]

for repo in repos:
    sage.analyze_repository(repo["url"], mode=repo["mode"])

# Cross-repository queries
response = sage.query(
    "Compare how FastAPI and the full-stack template handle authentication",
    scope="all"  # Search across all analyzed repositories
)
```

### Performance Optimization

- **Large Repositories**: Use `--max-files` flag to limit analysis scope
- **Memory Constraints**: Reduce embedding batch size and chunk size
- **Speed**: Use SSD storage for ChromaDB and enable model caching

### Debugging

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG

# Run with debugging
python -m git_sage --debug analyze <repository-url>

# Check logs
tail -f logs/git_sage.log
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/Ahnaf19/git-sage.git
cd git-sage

# Quick setup using Make
make setup
make install

# OR manual setup
conda env create -f environment.yml
conda activate gitsage
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### Areas for Contribution

- **Language Support**: Add Tree-sitter parsers for more languages
- **Model Integration**: Support for additional LLM providers
- **UI/UX**: Web interface or VS Code extension
- **Performance**: Optimization for large repositories
- **Documentation**: Examples and tutorials

## Learning Objectives

This project demonstrates:

- **LLM Application Architecture** with local models
- **Vector Database Integration** for semantic search
- **Code Analysis Techniques** using Tree-sitter
- **Embedding Generation** for code understanding
- **CLI Development** with Python
- **Repository Management** and Git operations

Perfect for learning how to build AI-powered developer tools and understanding modern LLM application patterns!

## License

Distributed under the [Apache License 2.0](LICENSE).  
You are free to use, modify, and distribute this project in accordance with the license terms.
