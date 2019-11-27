#!/bin/bash
cd /home/devp1/Documents/projects/project_10/substitute/management/commands
source ../../../venv/bin/activate
export DJANGO_SETTINGS_MODULE="nutella.settings.production"
python ../../../manage.py updatedb