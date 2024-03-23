# HSE_MC_ML_Project


## Description

Application detect faces at 'data/Marty&Brown.png' and shows it.


## Setup project

Install poetry (https://python-poetry.org/docs/#installation)

Install dependencies

```poetry install```


## Build package from source code

```python3 -m build .```

or via poetry

```poetry build```


## Install from github and run

```pip3 install git+https://github.com/jacksonrr3/HSE_MC_ML_Project.git```

```demo```


## Local development

### Run style linting tools

```black .```
```isort .```


### Run code linting tools

```flake8 .```


### Pre-commit hooks is run every commit auto

Run to set up the git hook scripts

```pre-commit install```

Run it malualy:

```pre-commit run --all-files```
Will show demo picture with borders around detected faces.


### Tests

run tests:
```pytest ./tests```


## Run application

```streamlit run app.py```

## Run with Docker

```docker build -t streamlit .```

```docker run -p 8501:8501 streamlit```

If all went well, you should see an output similar to the following:

    docker run -p 8501:8501 streamlit

    You can now view your Streamlit app in your browser.

    URL: http://0.0.0.0:8501```
