import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys

def combined_features(row):
    return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']

def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]

def get_title_from_index(index):
    if df[df.index == index]["title"].values.size:
        return df[df.index == index]["title"].values[0]
    return False

df = pd.read_csv("movie_dataset.csv")

df_syn = pd.read_csv("../Data/movie_synopsis.csv")

movies_syn = set(df_syn['title'])

movies_eval = set(df['title'])

inter = movies_eval.intersection(movies_syn)

for title in movies_eval:
    if title not in inter:
        df = df[df.title != title]


features = ['keywords', 'cast', 'genres', 'director']
for feature in features:
    df[feature] = df[feature].fillna('')

df["combined_features"] = df.apply(combined_features, axis =1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

cosine_sim = cosine_similarity(count_matrix)

def get_most_similar(movie_user_likes):
    movie_index = get_index_from_title(movie_user_likes)

    similar_movies = list(enumerate(cosine_sim[movie_index]))

    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
    titles = []
    i=1
    while len(titles)<10 and i<len(sorted_similar_movies):
        if get_title_from_index(sorted_similar_movies[i][0]):
            titles.append(get_title_from_index(sorted_similar_movies[i][0]))
        i+=1
    return titles


if __name__ == '__main__':

    for line in get_most_similar(sys.argv[1]):
        print(line)

