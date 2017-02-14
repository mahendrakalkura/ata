System Requirements
===================

- Git
- NPM
    - Bower
- Python 2.7
    - pip
    - virtualenvwrapper

How to install?
===============

```
$ mkdir ata
$ cd ata
$ git clone --recursive git@github.com:mahendrakalkura/ata.git .
$ cp ata/settings_local.py.sample ata/settings_local.py (edit as required)
$ mkvirtualenv ata
$ workon ata
$ pip install -r requirements.txt
$ bower install
$ python manage.py assets build
```

How to run?
===========

```
$ cd ata
$ workon ata
$ python manage.py runserver
$ xdg-open http://127.0.0.1:8000/
```

How to test?
============

```
$ aws ecr get-login --region us-west-2
$ docker login ...
$ docker pull .../advancedthreatanalytics/helloworld:1.0
$ docker run .../advancedthreatanalytics/helloworld:1.0
$ xdg-open http://127.0.0.1:8000/
- See "Check" button in the "Update Available?" column
- Click the "Check" button in the "Update Available?" column
- See "latest" button in the "Update Available?" column
- Click the "latest" button in the "Update Available?" column
```
