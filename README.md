# Spark Equation trial task

This code base serves as the trial task for Python developers.

## Code characteristics

* Works on Python py36, py37, py38

## Setting up a development environment

We assume that you have `Pipenv` installed.

    pipenv sync --dev


# Adding settings

Copy the `local_settings_example.py` file to `local_settings.py`.

    cp app/local_settings_example.py app/local_settings.py

Edit the `local_settings.py` file.


## Initializing the Database

    # Create DB tables and populate the tables
    python manage.py db upgrade


## Running the app

    # Start the Flask development web server
    python manage.py runserver

Point your web browser to http://localhost:5000/products


## Running the automated tests

    # Run tests
    py.test tests/


## Trouble shooting

If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app.sqlite`.
