# Flask by Example
## Part One: Set up a local development environment and then deploy both a staging and a production environment on Heroku.

## Part Two: Set up a PostgreSQL database along with SQLAlchemy and Alembic to handle migrations. (current)

## Part Three: Add in the back-end logic to scrape and then process the word counts from a webpage using the requests, BeautifulSoup, and Natural Language Toolkit (NLTK) libraries.


## Installation
```bash
$ sudo -H pip3 install -U pipenv # only if pipenv is not installed in system

$ pipenv --python 3.6
$ pipenv shell

$ pip install -r requirements.txt
```

## Set up PostgreSQL
```bash
$ sudo su - postgres
$ psql
# create database wordcount_dev;
# \q
```

## Run Project
```bash
$ source .env
$ python manage.py db upgrade
```

## License
[MIT](https://choosealicense.com/licenses/mit/)