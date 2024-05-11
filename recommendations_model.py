import pandas as pd  # pandas is used for data manipulation and analysis
import numpy as np
import os
import tensorflow as tf
import pickle
import matplotlib.pyplot as plt
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity  # For computing cosine similarity between vectors
from sklearn.neighbors import NearestNeighbors  # For implementing k-nearest neighbors algorithm
from sklearn.decomposition import PCA  # For performing Principal Component Analysis (PCA)
from sklearn.neighbors import NearestNeighbors


def embed(texts):
    model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    print('model loaded')
    # Use the pre-trained model to obtain embeddings for the input 'texts'
    # The 'model' variable is assumed to be loaded with a pre-trained model from TensorFlow Hub
    return model(texts)


def load_data():
    df = pd.read_csv('mymoviedb.csv')
    df.head()
    df['Poster_Url'][0]
    # Select only the columns "Title", "Overview", and "Poster_Url" from the DataFrame 'df'
    # The DataFrame 'df' is assumed to have columns named "Title", "Overview", and "Poster_Url"

    df = df[["Title", "Overview", "Poster_Url"]]

    # Display the first few rows of the modified DataFrame 'df'
    df.head()

    # *Data Cleaning*
    # Check for missing values in each column of the DataFrame 'df'
    df.isnull().sum()

    # Check for duplicate rows in the DataFrame 'df'
    df.duplicated().sum()
    has_duplicates = df.duplicated().any()
    print(has_duplicates)

    return df


def recommend(text,nn,movies):
    # Generate the embedding for the input 'text' using the 'embed' function
    emb = embed([text])

    # Find the 10 nearest neighbors based on the computed embeddings using the NearestNeighbors model 'nn'
    neighbors = nn.kneighbors(emb, return_distance=False)[0]

    # Print the titles of the recommended movies based on the nearest neighbors

    recommended_movies = [movies['Title'].iloc[i] for i in neighbors]
    return recommended_movies


def before_serevr():
    movies = load_data()

    titles = list(movies['Overview'])

    embeddings = embed(titles)
    print('The embedding shape is: ', embeddings.shape)

    pca = PCA(n_components=2)
    emb_2d = pca.fit_transform(embeddings)

    plt.figure(figsize=(11, 6))
    plt.title("Embedding space")
    plt.scatter(emb_2d[:, 0], emb_2d[:, 1])
    plt.show()

    nn = NearestNeighbors(n_neighbors=10)

    nn.fit(embeddings)
    return nn,movies
if __name__ == '__main__':
    movies = load_data()

    titles = list(movies['Overview'])

    embeddings = embed(titles)
    print('The embedding shape is: ', embeddings.shape)

    pca = PCA(n_components=2)
    emb_2d = pca.fit_transform(embeddings)

    plt.figure(figsize=(11, 6))
    plt.title("Embedding space")
    plt.scatter(emb_2d[:, 0], emb_2d[:, 1])
    plt.show()

    nn = NearestNeighbors(n_neighbors=10)
    # Its important to use binary mode
    # knnPickle = open('knnpickle_file', 'wb')
    #
    # # source, destination
    # pickle.dump(nn, knnPickle)
    #
    # # close the file
    # knnPickle.close()
    #
    # # load the model from disk
    # loaded_model = pickle.load(open('knnpickle_file', 'rb'))
    # result = loaded_model.predict("Batman")
    nn.fit(embeddings)
    recommend('Batman',nn)