#!/bin/bash
cd /home/sandrinesuire/project_10/substitute/management/commands
source ../../../../venv/bin/activate
export DJANGO_SETTINGS_MODULE="nutella.settings.production"
<<<<<<< HEAD
python ../../../manage.py updatedb
=======
python ../../../../manage.py updatedb
>>>>>>> d9a68752a332f136e9e4644b4e8178e7506c820c
