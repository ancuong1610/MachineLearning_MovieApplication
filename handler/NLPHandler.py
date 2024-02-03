import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


class NLPHandler:
    def __init__(self):
        self.df = pd.read_csv('../templates/tmdb_5000_movies.csv')

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
        return self.df.loc[index, 'overview']
