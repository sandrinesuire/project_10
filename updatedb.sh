#!/bin/bash
cd /home/sandrinesuire/project_10/substitute/management/commands
source ../../../../env/bin/activate
export DJANGO_SETTINGS_MODULE="nutella.settings.production"
python ../../../manage.py updatedb
