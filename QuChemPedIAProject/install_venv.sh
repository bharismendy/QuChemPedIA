#!/bin/bash

echo "suppression du dossier venv..."
rm -rf venv
echo "création de l'environement virtuel..."
virtualenv venv -p python3.5
echo "installation des package python..."
source venv/bin/activate
venv/bin/pip3.5 install -r requirements.txt 
deactivate
echo "fin de l'installation de l'environement virtuel ..."
