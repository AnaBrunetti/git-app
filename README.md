# Overview
GitHub APP integration [POC]

# Requirements

* Python (3.11.0) [Installation](https://www.python.org/downloads/ "Installation") 
* Virtualenv (20.16.6) [Installation](https://pypi.org/project/virtualenv/20.16.6/ "Installation")
* Visual Studio Code (Recomended IDE) [Installation](https://code.visualstudio.com/ "Installation")

# Run project
* Git clone this repository.
* Open ide and project folder (vs used).
* Change APP variables at utils.py
* At terminal: <br>
 ```
$ pip install virtualenv
$ python -m virtualenv venv -p python
$ ./venv/scripts/activate
$ pip install -r requirements.txt
$ cd app
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
 ```
* Access http://127.0.0.1:8000/ or http://localhost:8000/
