##############################################################
#                                                            #
#                     IMPORTATION DES MODULES                #
#                                                            #
##############################################################

import csv # Lecture du corpus
import pickle # Sauvegarde des embeddings

# Typage des fonctions
from typing import List, Tuple
from sentence_transformers import SentenceTransformer

##############################################################

def read_corpus(corpus_path: str) -> List[Tuple[str, str]]:
    """Renvoie le corpus sous la forme d'une liste de tuples (title, synopsis)
    
    Args: 
        corpus (str): chemin vers le corpus au format csv
        
    Returns:
        List[Tuple[str, str]]: le corpus sous la forme d'une liste de tuples
        (title, synopsis)
    """

    with open(corpus_path, encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        
        # Récupération des données sous la forme d'une liste de tuples
        corpus = [(line["title"], line["synopsis"]) for line in csv_reader]
        
    return corpus

def make_embeddings_corpus(corpus: List[Tuple[str, str]], model: SentenceTransformer) -> List[Tuple]:
    """Renvoie une liste de tuples (embedding_movie, title, synopsis)
    
    A partir du modèle SentenceTransformer fourni, la fonction crée les embeddings
    pour le synopsis de chaque oeuvre. Le résultat de la fonction est une liste
    de tuples où chaque tuple contient l'embedding du synopsis d'une oeuvre donnée, 
    le titre de l'oeuvre en question et le synopsis. 

    Args:
        corpus (List[Tuple[str, str]]): Le corpus sous la forme d'une liste de tuples (title, synopsis)
        model (SentenceTransformer): le modèle utilisé pour créer les embeddings

    Returns:
        List[Tuple]: liste de tuples (embedding_movie, title, synopsis)
    """
    embeddings_corpus = [] 
    for title, synopsis in corpus:
        embeddings_corpus.append(
            (
                model.encode(synopsis), # Embedding du synopsis créé avec le modèle
                title,
                synopsis
            )
        ) 
    return embeddings_corpus

##############################################################
#                                                            #
#                             MAIN                           #
#                                                            #
##############################################################

if __name__ == "__main__":
    
    # Main utilisé pour la création du fichier `app/embeddings/embeddings_corpus_movie`
    # Utilisé une seule fois car c'est pour la version de l'API avec le modèle non-finetuné
    
    # Lecture du corpus
    corpus = read_corpus("../../../Data/movie_synopsis.csv")
    
    # Chargement du modèle
    model = SentenceTransformer(model_name_or_path='sentence-transformers/all-MiniLM-L6-v2')

    # Liste contenant toutes les oeuvres sous la forme d'un tuple (embedding, tile, synopsis)
    oeuvres = make_embeddings_corpus(corpus=corpus, model=model)
    
    # Sauvegarde du modèle
    model.save("../../models/sentence_similarity_model")
    
    # Sauvegarde des embeddings dans un fichier pickled
    with open("../../embeddings/embeddings_corpus_movie", "wb") as embedding_corpus_file:
        pickle.dump(oeuvres, embedding_corpus_file)