# json-api
Main => ![example workflow](https://github.com/iamr0b0tx/json-api/actions/workflows/django.yml/badge.svg?branch=main) <br>
Dev ==> ![example workflow](https://github.com/iamr0b0tx/json-api/actions/workflows/django.yml/badge.svg?branch=dev) <br>
Indev => ![example workflow](https://github.com/iamr0b0tx/json-api/actions/workflows/django.yml/badge.svg?branch=indev) <br>
A JSON API

### Tools and Resources
1. Python 3.6+
2. Virtualenv

Make sure to download/clone this repository and navigate to the folder in your terminal. Now follow the instructions below

1. Create the virtual environment.
```
    virtualenv /path/to/venv --python=/path/to/python3
```
You can find out the path to your `python3` interpreter with the command `which python3`.

2. Set up `.env` file by duplicating the `.example.env` file(and editing if required).

3. Activate the environment and install dependencies.
    - #### Linux
    ```
        source /path/to/venv/bin/activate
        pip install -r requirements\dev.linux.txt
    ```

    - #### Windows
    ```
        ./path/to/venv/bin/activate
        pip install -r requirements\dev.windows.txt
    ```

4. Launch the service
```
    python manage.py runserver```

## Posting requests locally
When the service is running, try this link in your browser/Postman. send a GET request
```
    127.0.0.1:8008/posts
```

You can test the project with pytest by running the command. You can check Github Actions for the status of tests [here](https://github.com/iamr0b0tx/uuid-api/actions) 
```
    pytest
```