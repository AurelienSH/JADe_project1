##############################################################
#                                                            #
#                     IMPORTATION DES MODULES                #
#                                                            #
##############################################################

import csv # Lecture du corpus

# Typage des fonctions
from typing import List, Tuple
from sentence_transformers import SentenceTransformer

##############################################################

def read_corpus(corpus_path: str) -> List[Tuple[str, str]]:
    """Renvoie le corpus sous la forme d'une liste de tuples (title, synopsis)"""

    with open(corpus_path, encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        
        # Récupération des données sous la forme d'une liste de tuples
        corpus = [(line["title"], line["synopsis"]) for line in csv_reader]
        
    return corpus

def make_embeddings_corpus(corpus: List[Tuple[str, str]], model: SentenceTransformer) -> List[Tuple]:
    """Crée une liste de listes [embedding_movie, title, synopsis]

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