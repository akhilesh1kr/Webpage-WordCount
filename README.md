# WebPage WordCount

This application counts the words in the webpage returned by user-submitted url.

## Technology used
```
Flask
PostgreSQL
Redis
```

## Installation
```bash
$ sudo -H pip3 install -U pipenv # only if pipenv is not installed in system

$ pipenv --python 3.6
$ pipenv shell

$ pip install -r requirements.txt

# PostgreSQL Installation
$ sudo apt update
$ sudo apt install postgresql postgresql-contrib

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
$ python manage.py runserver

# Open another Tab on Terminal
$ python worker.py
```

## Redis Installation
```
Download, extract and compile Redis with:

$ wget http://download.redis.io/releases/redis-5.0.3.tar.gz
$ tar xzf redis-5.0.3.tar.gz
$ cd redis-5.0.3
$ make

The binaries that are now compiled are available in the src directory. Run Redis with:

$ src/redis-server
```

## Downloading NLTK (though Tokenizer is already added in git project)
```
$ python -m nltk.downloader

When the installation window appears, update the ‘Download Directory’ to absolute_path_to_your_app/nltk_data/.

Then click the ‘Models’ tab and select ‘punkt’ under the ‘Identifier’ column. Click ‘Download’.
```

## License
[MIT](https://choosealicense.com/licenses/mit/)