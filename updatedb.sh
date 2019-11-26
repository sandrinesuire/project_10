#!/bin/bash
cd /home/sandrinesuire/project_10/substitute/management/commands
source ../../../../env/bin/activate
export DJANGO_SETTINGS_MODULE="nutella.settings.production"
<<<<<<< HEAD
python ../../../manage.py updatedb
=======
python ../../../manage.py updatedb
>>>>>>> 1164aa02a1c1a0921426295a9383cfbfa5875ea4
