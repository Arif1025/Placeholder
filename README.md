# Team Placeholder Big Group Project

## Team members
The members of the team are:
 - Jasmin Bedi
 - Manav Sukheja
 - Khuslen Bambar
 - Aman Hayer
 - Joshua Hodes
 - Arif Uddin
 - Chuhao (Akalay) Weng
 - Sanika Gadgil


## Project structure
This project is called Interactive Polling System. It currently consists of a single app 'polls'.

## Deployed version of the application
The deployed version of the application can be found at [enter url here].

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment. From the root of the project:

$ virtualenv venv
$ source venv/bin/activate


Install all required packages:

$ pip3 install -r requirements.txt


Migrate the database:

$ python3 manage.py migrate


Seed the development database with:

$ python3 manage.py seed


Run all tests with:
$ python3 manage.py test
