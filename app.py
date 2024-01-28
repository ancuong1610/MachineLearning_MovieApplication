import subprocess
from flask import Flask, render_template, request, send_from_directory
from string import Template
from SPARQLWrapper import SPARQLWrapper, JSON
import requests

# choose the correct version for your computer
fuseki_path = 'apache-jena-fuseki-4.9.0/fuseki-server'  # Unix machine
#fuseki_path = 'apache-jena-fuseki-4.9.0/fuseki-server.bat'  # Window machine
ttl_file_path = 'TMDB.ttl'




sparql = SPARQLWrapper("http://localhost:3030/TMDB/query")  # check http://localhost:3030 for SPARQL Endpoint before run
sparql.setReturnFormat(JSON)
actor_query = """
PREFIX : <https://www.themoviedb.org/kaggle-export/>
SELECT ?actor
WHERE{
?m a :Movie ;
:title "$title" ;
:cast/:name ?actor .
}
"""


def query(title):
    query_string = Template(actor_query).substitute(title=title)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    results = [row['actor']['value'] for row in results_dict['results']['bindings']]
    return results


app = Flask(__name__)


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        title = request.form['title']
        return render_template('index.html', actors=query(title))
    else:
        return render_template('index.html', actors=[])

@app.route("/actor", methods=('GET', 'POST'))
def actor():
    if request.method == 'POST':
        title = request.form['title']
        return render_template('index2.html', actors=query(actor))
    else:
        return render_template('index2.html', actors=[])

@app.route("/genre", methods=('GET', 'POST'))
def genre():
    if request.method == 'POST':
        title = request.form['title']
        return render_template('index3.html', actors=query(genre))
    else:
        return render_template('index3.html', actors=[])

@app.route("/description", methods=('GET', 'POST'))
def description():
    if request.method == 'POST':
        title = request.form['title']
        return render_template('index4.html', descript=query(description))
    else:
        return render_template('index4.html', descript=[])
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run()
