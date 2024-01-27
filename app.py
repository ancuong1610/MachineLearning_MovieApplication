from flask import Flask, render_template, request, send_from_directory
from string import Template
from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("http://localhost:3030/TMDB/sparql")
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
   app.run()
