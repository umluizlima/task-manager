# task-manager
[![Build Status](https://travis-ci.org/umluizlima/task-manager.svg?branch=master)](https://travis-ci.org/umluizlima/task-manager)

Application to manage tasks built following [cassiobotaro/do_zero_a_implantacao](https://github.com/cassiobotaro/do_zero_a_implantacao/blob/master/README.md)

## Development

### Requirements
- Python 3.7+
- Docker
- Docker Compose

### Installing
Install dependencies
```console
make install
```

### Testing
```console
make test
```

### Running
Access the API documentation on http://localhost:8000/docs
```console
make run
```

### Migrating
Generate migration files automatically for changes to models. Make sure all models are imported on `database.py`
```console
make db_generate_migration description="your description"
```
