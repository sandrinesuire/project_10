# Create a platform for Nutella lovers

## Objective of the project

The startup Pur Beurre, wants to develop a web platform for its customers. This site will allow anyone to find a 
healthy substitute for a food considered "Too fat, too sweet, too salty" (although we all know that fat is life).


## Specifications

The specifications are available in jointed file cahier_des_charges.docx.


## Deliverables

* Link to your site in production, fully functional.
* Written document explaining your creative process, the difficulties encountered and the way you solved them. Include 
the link to your Trello board or Pivotal Tracker, the link to your Github repo and the site in production. The document 
must be in pdf format and not exceed 2 A4 pages. It can be written in either English or French, but take into 
consideration that spelling and grammar mistakes will be evaluated!


## Constraints
* Tests: test your project by adopting the approach that seems most appropriate (TDD or tests written at the end of a 
feature)
* Use a PostgreSql database instead of MySQL, otherwise you will not be able to deploy your application on Heroku.
* Include a page "Legal Mentions" which will contain the coordinates of the host and the authors of the various free 
resources used (template, photos, icons, ...).
* Follow the best practices of PEP 8
* Pause your code regularly on Github and create PR when you want your mentor back.
* Your code must be fully written in English: functions, comments, ...
* Use an agile project methodology to work in project mode.


## Install

Virtual environment Linux
```
pip install virtualenv
virtualenv -p python3 env
source env/bin/activate
```
Install the libraries
```
pip install -r requirements.txt
```

## Play
 
Start the plateform application in development mode :
 * create database nutella on 127.0.0.1:5432 with "sandrine" user and "sandrine" password 
```
python manage.py migrate
python manage.py runserve
```

## Test
 
```
python manage.py test
```

## Platforms

This application was testing on
* Ubuntu 18.10 + python 3.6.7
