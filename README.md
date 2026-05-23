# mini-rag

This is a minimal implementation of the RAG model for question answering

## Requirements
- python 3.14.4 or later


## Installation

### Install the required packages

```bash
pip install -r requirements.txt
```

### setup your environment of keys

```bash
cp .env.example .env
```
set your environment variables in the `.env` file Like `OPEN_API_KEY` value


## Running app

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```