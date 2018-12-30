import os
import requests
import operator
import re
import nltk
import time
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup

from rq import Queue
from rq.job import Job
from worker import conn


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

q = Queue(connection=conn)

from models import *


def count_words_at_url_and_save(url):

    errors = []

    try:
        r = requests.get(url)
    except:
        errors.append(
            "Unable to get URL. Please make sure it's valid and try again."
        )
        return {"error": errors}

    # text processing
    raw = BeautifulSoup(r.text, 'html.parser')
    while raw.script != None:
        raw.script.extract() # prevent the analysis of script content
    while raw.style != None:
        raw.style.extract() # prevent the analysis of style content

    raw = raw.get_text()
    nltk.data.path.append('./nltk_data/')  # set the path
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    # remove punctuation, count raw words
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)

    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)

    # save the results
    try:
        result = Result(
            url=url,
            result_all=raw_word_count,
            result_no_stop_words=no_stop_words_count
        )
        # print(result)
        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}


@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        url = request.form['url']
        if 'http://' not in url[:7] and 'https://' not in url[:8]:
            url = 'http://' + url
        job = q.enqueue_call(
            func=count_words_at_url_and_save, args=(url,), result_ttl=5000
        )
        print("job id:")
        print(job.get_id())
        job_id = job.get_id()
        time.sleep(2)
        return redirect(url_for('get_results', job_key=job_id))

    return render_template('index.html', results=results)



@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    print(job_key)
    job = Job.fetch(job_key, connection=conn)
    # print(job)
    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        # print(result)
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:20]
        # return jsonify(results)
        return render_template('index.html', results=results)
    else:
        return "Oops, Either <i>Job Listener or Redis Server</i> is shut down <br> OR <br> Else, data was on its way.. Please Refresh", 202


if __name__ == '__main__':
    app.run()