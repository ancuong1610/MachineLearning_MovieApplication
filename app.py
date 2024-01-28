import subprocess
from flask import Flask, render_template, request, send_from_directory
from string import Template
from SPARQLWrapper import SPARQLWrapper, JSON
import requests

# choose the correct version for your computer
fuseki_path = 'apache-jena-fuseki-4.9.0/fuseki-server'  # Unix machine
#fuseki_path = 'apache-jena-fuseki-4.9.0/fuseki-server.bat'  # Window machine
ttl_file_path = 'TMDB.ttl'


def start_fuseki_server():
    subprocess.Popen([fuseki_path, '--update', '--mem', '/TMDB'])  # Unix machine
    #subprocess.Popen(fuseki_path + ' --update --mem /TMDB', shell=True)  # Window machine

    import time
    time.sleep(5)

    upload_ttl_to_fuseki()


def upload_ttl_to_fuseki():
    data = open(ttl_file_path).read()
    headers = {'Content-Type': 'text/turtle;charset=utf-8'}
    fuseki_url = 'http://localhost:3030/TMDB/data?default'
    response = requests.post(fuseki_url, data=data, headers=headers)

    if response.status_code == 200:
        print("TMDB.ttl file uploaded successfully to Fuseki server.")
    else:
        print(f"Failed to upload TMDB.ttl. Status code: {response.status_code}")


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


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    start_fuseki_server()
    app.run()
