# AI Learning Platform

## Setup Project Locally

### Virtual Environment

Create the python Virtual Environment using Python 3

```bash
python3 -m venv .venv
```

### Activate Virtual Environment

Activate the corresponding virtual environment by running code below

```bash
. .venv/bin/activate
```

### Install requirements

Run the code below to install libraries and framework from requirements.txt

```bash
pip install -r requirements.txt 
```

### Initialize Database File

Run the init-db command:

```bash
flask --app flaskr init-db
# Initialized the database.
```

There will now be a flaskr.sqlite file in the instance folder in your project.

### Run the project locally

```bash
flask --app flaskr run --debug
```

This will start the application in a debug mode and open a port on `5000`
The project will be accessible on the browser running on `http://127.0.0.1:5000`
