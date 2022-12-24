# Django Development

# Menu

* [Requirements](#requirements)
* [Installation](#installation)
* [Initial Setup](#initial-setup)
* [Virtual Environment](#virtual-environment)
* [Django Setup](#django-setup)


## Requirements:

We need the follwing:
- Github Account
- Docker Account
- AWS Account
- Python Installed in our PC
- Django framework installed in our PC
- Virtual environment of Python provisions
- Django Rest Framework installed in our PC
- VS Code

## Installation

### Github (GIT-SCM)

* Install git-scm from https://git-scm.com/downloads
* Run the exe file and connect to your git hub account

### Python

* Install Python from https://www.python.org/downloads/ 
* Run the python.exe and intall with the pip and all environment variable facility

### Docker

* Instal Docker Desktop from https://www.docker.com/products/docker-desktop/
* Create an account in the Docker website and link it to the docker desktop


## Initial Setup
- Create a folder *recipe-app-api*
- Create a new github repository inside the new folder created
- Connect the repository and the file
- Commands:

```bash
> mkdir recipe-app-api
> cd recipe-app-api
recipe-app-api> git init
recipe-app-api> git add .
recipe-app-api> git commit -m "first commit"
recipe-app-api> git remote add origin <add your repository link here>
recipe-app-api> git push -u origin master
```

## Virtual Environment
Here we activate the virtual environment and work with Django in this environment

### Virtual environment installation
```bash
recipe-app-api> pip install venv
recipe-app-api> python3 -m venv env
```

### Activate the environment:
```bash
recipe-app-api> env\Scripts\activate
```
or
```bash
recipe-app-api> source env/Scripts/activate
```

## Django Setup

*Always activate the virtual environment* Learn from : [activate virtual environment](#virtual-environment)

### Django Installation

*Run the follwing to install the django and djangorestframework*
```bash
(env) recipe-app-api> pip install django djangorestframework
```

*Now create the requirement.txt file*
```bash
(env) recipe-app-api> pip freeze > requirement.txt
```

### Django App

Start the project with:
```bash
(env) recipe-app-api> django-admin startproject recipeapp .
```

Run the project server with:
```bash
(env) recipe-app-api> python3 manage.py runserver
```
