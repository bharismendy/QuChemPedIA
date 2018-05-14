
# Mise en place de l'environement
## Installation

### pour commencer mettons à jour notre système :
	 sudo apt-get update && apt-get upgrade -y
	 
### installation de postgreSQL ([CF](https://www.howtoforge.com/tutorial/ubuntu-postgresql-installation/))
	sudo apt-get -y install postgresql postgresql-contrib phppgadmin
	
### installation de virtualenv with python3
	cd /location
	virtualenv -p python3 nameOfEnv
	source /path/to/the/directory/of/env
	
### installation de django 
	pip install django
	
### librairie utilisé :
	elasticsearch_dsl
	django-rest-framework
	elasticsearch
	psycopg2-binary==2.7.4
    django-bootstrap4

### to Generate a requirements file
	pip freeze > requirements.txt

### to Install the packages
	pip install -r requirements.txt
	
### to relocate the virtual env
	virtualenv --relocatable ENV
	
### installation du module de communication avec postgre
	pip install psycopg2-binary

### Read the doc here :
	https://virtualenv.pypa.io/en/stable/userguide/
 
## Configuration
### creation du superutilisateur django
	python manage.py createsuperuser

### Set up database :
	create an user : "dataSlave", password : "P@ssw0rd"
	and a database : "QuChemPedIADB"
	to ask django to set up the connection with database :
	python manage.py makemigrations QuChemPedIA
	python manage.py migrate
