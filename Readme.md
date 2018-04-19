
# Mise en place de l'environement
## Installation

### pour commencer mettons à jour notre système :
	 sudo apt-get update && apt-get upgrade -y
### installation de postgreSQL ([CF](https://www.howtoforge.com/tutorial/ubuntu-postgresql-installation/))
	sudo apt-get -y install postgresql postgresql-contrib phppgadmin
### installation de virtualenv
	cd /location
	virtualenv nameOfEnv
	source /path/to/the/directory/of/env
### installation de django 
	pip install django
### installation du module de communication avec postgre
	pip install psycopg2-binary


## Configuration
### creation du superutilisateur django
	python manage.py createsuperuser

