from SPARQLWrapper import SPARQLWrapper, JSON
from string import Template

class KnowledgeGraphHandler:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://localhost:3030/TMDB/query")
        self.sparql.setReturnFormat(JSON)

    def query_actors_by_title(self, title):
        actor_query = """
        PREFIX : <https://www.themoviedb.org/kaggle-export/>
        SELECT ?actor
        WHERE {
            ?m a :Movie ;
            :title "$title" ;
            :cast/:name ?actor .
        }
        """
        query_string = Template(actor_query).substitute(title=title)
        self.sparql.setQuery(query_string)
        results_dict = self.sparql.query().convert()
        results = [row['actor']['value'] for row in results_dict['results']['bindings']]
        return results

    def query_movie_by_gerne(self,gerne):
        film_query = """
        PREFIX : <https://www.themoviedb.org/kaggle-export/>
        SELECT ?movie
        WHERE{
            ?m a :Movie ;
            :genres ?genres ;
            :title ?movie.
            ?genres :name "$genre" .
        }
        """
        query_string = Template(film_query).substitute(gerne=gerne)
        self.sparql.setQuery(query_string)
        results_dict = self.sparql.query().convert()
        results = [row['movie']['value'] for row in results_dict['results']['bindings']]
        return results
