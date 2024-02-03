import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import os


class NLPHandler:
    def __init__(self):
        # Get the directory that this script is in
        script_dir = os.path.dirname(__file__)
        # Construct the path to the CSV file
        csv_path = os.path.join(script_dir, 'tmdb_5000_movies.csv')
        # Now you can use csv_path to read the CSV file
        self.df = pd.read_csv(csv_path)

        # Not available values to empty String
        self.df['overview'] = self.df['overview'].fillna('')
        self.vectorizer = TfidfVectorizer()

        # overview column = description
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['overview'])

        self.model = NearestNeighbors(metric='cosine')
        self.model.fit(self.tfidf_matrix)

    def get_movie_description(self, title):
        title_vector = self.vectorizer.transform([title])
        distances, indices = self.model.kneighbors(title_vector)
        # index of nearest movie
        index = indices[0][0]
        print([self.df.loc[index, 'overview']])
        return [self.df.loc[index, 'overview']]


#if __name__ == '__main__':
#    nlp = NLPHandler()
#    print(nlp.get_movie_description("Oz"))
