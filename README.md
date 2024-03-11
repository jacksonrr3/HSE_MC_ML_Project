# HSE_MC_ML_Project

## Description

Application runs video from 'data/demo.mp4' folder and detect faces.

## Requirments for local development

install Python3
install Poetry


## Setup and run manualy

All commands run from project folder. Operation system - Ubuntu 20.

1. Create Python virtual environment

```python -m venv /path/to/new/virtual/environment```

2. Activate Python virtual environment

```source <venv>/bin/activate```

3. Install dependencies

```pip install -r requirements.txt```

4. Run demo

```python ./src/demo/demo.py ```


## Build package from source code

```python3 –m build .```

or via poetry

```poetry build```


## Install from github and run


```pip3 install git+https://github.com/jacksonrr3/HSE_MC_ML_Project@1_week```


```demo```


## Local development

### Run style linting tools

```black .```
```isort .```

### Run code linting tools

```flake8 .```

### Pre-commit hooks is run every commit auto
Run it malualy:

```pre-commit run --all-files```
