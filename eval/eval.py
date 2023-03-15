from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import pickle
import pandas as pd
import sys
from os import path
import os
from datetime import date

# Ajout du chemin des modules utilisés
sys.path.append('../app')

# Récupération de la fonction permettant de générer les recommandations
from src.scripts.similarity import get_similar_works

models_path = "../app/models"
embeddings_path = "../app/embeddings"
qp = "queries/"

# Récupération du modèle non fine-tuné
model_1 = SentenceTransformer(f"{models_path}/sentence_similarity_model")

# Récupération du modèle fine-tuné
model_2 = SentenceTransformer(f"{models_path}/sentence_similarity_model_FT")

# Récupération des embeddings du modèle non fine tuné
with open(f"{embeddings_path}/embeddings_corpus_movie", "rb") as f:
    embeddings_nonFT = pickle.load(f)

# Récupération des embeddings du modèle fine tuné
with open(f"{embeddings_path}/embeddings_FT_corpus_movie", "rb") as f:
    embeddings_FT = pickle.load(f)

# Conservations des informations liées aux modèles sous forme de tuples
models = [(model_1, 'nonFT', embeddings_nonFT), (model_2, 'FT', embeddings_FT)]

def read(style: str) -> pd.DataFrame:
    """
    Fonction permettant la lecture des fichiers de queries, des tsv dont les colonnes sont "title" et "synopsis"
    Args:
        typ (str) : le style des entrées à tester

    Returns:
        pd.DataFrame
    """
    return pd.read_csv(f"{qp}{style}.tsv", sep="\t")

def eval_v1(model : SentenceTransformer, embeddings : List[Tuple]) -> float:
    """
    Première version de l'évaluation donnant un score représentant à quel point les synopsis d'origines permettent de retrouver l'oeuvre cible
    Args:
        model (SentenceTransformer)
        embeddings (List[Tuple])
    Returns:
        score (float)
    """
    value = 0

    for _, title, syn in embeddings:
        # Pour chaque titre, on récupère le vecteur le plus proche
        best = get_similar_works(user_input= syn, oeuvres=embeddings, model=model)[0]['title']
        # Si ce film est celui qui est attendu, on le compte
        if best == title:
            value += 1

    # On divise le nombre de films correctements identifiés par la taille du corpus
    return value/len(embeddings)

def eval_v2(style : str,queries: pd.DataFrame, model: SentenceTransformer, model_name: str, embeddings: List[Tuple]) -> float:
    """
    Deuxième fonction d'évaluation, ici des synopsis écrits par des évaluateurs doivent etres utilisés.
    Ces synopsis doivent avoir une oeuvre cible se trouvant dans le corpus.
    Le score est basé sur le compte d'oeuvre cible se trouvant dans la liste de recommandations du synopsis.
    Args:
        style (str) : Le style du synopsis écrit (correspond au nom du fichier tsv devant être chargé)
        queries (pd.DataFrame): le dataframe des synopsis ciblés
        model (SentenceTransformer)
        model_name (str) : le nom que l'utilisateur souhaite donner au modèle à tester
        embeddings (List[Tuple])
    Returns:
        score (float)
    """
    score = 0

    # Vérification de l'existence d'un dossier pour le modèle à évaluer
    if not path.exists(f"results/{model_name}"):
        os.mkdir(f"results/{model_name}")

    # Boucle d'évaluation
    for index, row in queries.iterrows():

        title = row['title']
        syn = row['synopsis']

        # Génération des recommandations
        suggestions = [res['title'] for res in get_similar_works(user_input = syn, oeuvres = embeddings, model = model)]

        # Vérification de l'existence d'un dossier pour le style de synopsis
        if not path.exists(f"results/{model_name}/{style}"):
            os.mkdir(f"results/{model_name}/{style}")

        # Ecriture de fichiers contenant les recommandations pour chaque synopsis pour une évaluation plus qualitative
        with open(f"results/{model_name}/{style}/{title}.txt", "w") as f:
            for res in suggestions:
                print(res, file=f)


        # Vérification de la présence de l'oeuvre cible dans les recommandations
        if title in suggestions:
            score+=1

    # Division du score par la taile de l'échantillon
    score = score/len(queries)

    return score
def main():
    desc = read("desc")

    syns = read("syns")

    query = read("query")

    dfs = {'descriptions': desc, 'synopsis': syns, 'queries': query}

    for model, name, embeddings in models:
        for k, df in dfs.items():
            with open(f"scores_{name}.txt", "a") as scoref:
                print(f"____________________{date.today()}____________________")
                print(f"Score obtenu sur les synopsis de type {k} : {eval_v2(k, df, model, name, embeddings)}", file = scoref)

if __name__ == '__main__':
    main()