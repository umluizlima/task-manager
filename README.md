# task-manager
Application to manage tasks

## Development

### Requirements
- Python 3.7+

### Installing
```console
pip install -r dev-requirements.txt
pre-commit install
```

### Testing
```console
python -m pytest --cov=app
```

### Running
```console
uvicorn --reload app:app
```