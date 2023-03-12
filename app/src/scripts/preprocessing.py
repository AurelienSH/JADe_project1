from typing import List
import csv

def read_corpus(corpus_path: str) -> List[List[str]]:
    """Renvoie le corpus sous la forme d'une liste de listes [synopsis, title]"""

    with open(corpus_path, encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        
        # En-tête du CSV
        headers = csv_reader.fieldnames
        
        # Récupération des données sous la forme d'une liste de listes
        corpus = [[line["synopsis"], line["title"]] for line in csv_reader]
        
    return corpus

def make_embeddings_corpus(corpus: List[List], model):
    """Crée une liste de listes [embedding_movie, title, synopsis]

    Args:
        corpus (List[List[str]]): Le corpus sous la forme d'une liste de listes [title, synopsis]
        model (_type_): le modèle utilisé pour créer les embeddings

    Returns:
        List[List]: liste de listes [embedding_movie, title, synopsis]
    """
    embeddings_corpus = [] 
    for synopsis, title in corpus:
        embeddings_corpus.append(
            (
                model.encode(synopsis), # Embedding du synopsis créé avec le modèle
                title,
                synopsis
            )
        ) 
    return embeddings_corpus

