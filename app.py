import subprocess
from flask import Flask, render_template, request, send_from_directory
from string import Template
from SPARQLWrapper import SPARQLWrapper, JSON
import requests

from handler.KnowledgeGraphHandler import KnowledgeGraphHandler
from handler.NLPHandler import NLPHandler

# choose the correct version for your computer
fuseki_path = 'apache-jena-fuseki-4.9.0/fuseki-server'  # Unix machine
#fuseki_path = 'apache-jena-fuseki-4.9.0/fuseki-server.bat'  # Window machine
ttl_file_path = 'TMDB.ttl'

##NOTE: leave for later developement
# def start_fuseki_server():
#     subprocess.Popen([fuseki_path, '--update', '--mem', '/TMDB'])  # Unix machine
#     #subprocess.Popen(fuseki_path + ' --update --mem /TMDB', shell=True)  # Window machine
#
#     import time
#     time.sleep(5)
#
#     upload_ttl_to_fuseki()
#
# def upload_ttl_to_fuseki():
#     data = open(ttl_file_path).read()
#     headers = {'Content-Type': 'text/turtle;charset=utf-8'}
#     fuseki_url = 'http://localhost:3030/TMDB/data?default'
#     response = requests.post(fuseki_url, data=data, headers=headers)
#
#     if response.status_code == 200:
#         print("TMDB.ttl file uploaded successfully to Fuseki server.")
#     else:
#         print(f"Failed to upload TMDB.ttl. Status code: {response.status_code}")


app = Flask(__name__)
knowledge_graph_handler = KnowledgeGraphHandler()
nlp_handler = NLPHandler()


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        title = request.form['title']
        return render_template('index.html', actors=knowledge_graph_handler.query_actors_by_title(title))
    else:
        return render_template('index.html', actors=[])


@app.route("/actor", methods=('GET', 'POST'))  #not clear what does this page do
def actor():
    if request.method == 'POST':
        title = request.form['title']
        return render_template('index2.html', actors=knowledge_graph_handler.query_actors_by_title(title))
    else:
        return render_template('index2.html', actors=[])


@app.route("/genre", methods=('GET', 'POST'))
def genre():
    if request.method == 'POST':
        genre = request.form['genre']
        return render_template('index3.html', actors=knowledge_graph_handler.query_movie_by_gerne(genre))
    else:
        return render_template('index3.html', actors=[])


@app.route("/description", methods=('GET', 'POST'))
def description():
    if request.method == 'POST':
        title = request.form['title']
        return render_template('index4.html', descript=knowledge_graph_handler.query_movie_by_gerne(genre))
    else:
        return render_template('index4.html', descript=[])


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    # start_fuseki_server()
    app.run()
