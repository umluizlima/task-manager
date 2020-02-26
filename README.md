# task-manager
[![Build Status](https://travis-ci.org/umluizlima/task-manager.svg?branch=master)](https://travis-ci.org/umluizlima/task-manager)

Application to manage tasks built following [cassiobotaro/do_zero_a_implantacao](https://github.com/cassiobotaro/do_zero_a_implantacao/blob/master/README.md)

## Development

### Requirements
- Python 3.7+

### Installing
```console
pip install -r requirements-dev.txt
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

Access the API documentation on http://localhost:8000/docs