##############################################################
#                                                            #
#                     IMPORTATION DES MODULES                #
#                                                            #
##############################################################

from typing import List, Tuple
from collections import namedtuple
import csv
import sys
import pickle # Sauvegarde des objets

# Transformers
from sentence_transformers import SentenceTransformer

# Calcul de similarité
from sklearn.metrics.pairwise import cosine_distances


##############################################################
#                                                            #
#                     LECTURE DU CORPUS                      #
#                                                            #
##############################################################

def read_corpus(corpus_path: str) -> List[List[str]]:

    with open(corpus_path, encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        
        # En-tête du CSV
        headers = csv_reader.fieldnames
        
        # Récupération des données sous la forme d'une liste de listes
        corpus = [[line["id"], line["synopsis"], line["title"]] for line in csv_reader]
        
    return corpus
    

##############################################################
#                                                            #
#                    CALCUL DE SIMILARITE                    #
#                                                            #
##############################################################

def get_similar_works(user_input: str, oeuvres: List[Tuple], model: SentenceTransformer, k: int=5):
    
    # Vectorization de la requête de l'utilisateur avec le modèle
    input_encoded = model.encode(user_input)
    
    similars = []
    
    # Calcul de la distance cosinus entre chaque oeuvre 
    # de la liste d'oeuvre et la requête de l'utilisateur
    for (embedding_oeuvre, title, synopsis) in oeuvres:
        
        # Création résultat sous la forme d'un tuple (distance, title, synopsis)
        result = (cosine_distances([embedding_oeuvre], [input_encoded]), title, synopsis)
        
        # Stockage des résultats dans une liste
        similars.append(result)
    
    # Triage des résultats selon la distance par ordre croissant
    # Pour obtenir les oeuvres les plus proches 
    sorted_similars = sorted(similars, key=lambda x: x[0])
    
    return [{"title": title, "content": synopsis} for _, title, synopsis in sorted_similars[:k]]


##############################################################
#                                                            #
#                             MAIN                           #
#                                                            #
##############################################################

if __name__ == "__main__":
    
    # Lecture du corpus
    corpus = read_corpus("../../../Data/movie_synopsis.csv")
    
    # Chargement du modèle
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Vectorization des synopsis par le modèle
    embeddings = model.encode([synopsis for (_, synopsis, _) in corpus])

    # Liste contenant toutes les oeuvres sous la forme d'un tuple (embedding, tile, synopsis)
    oeuvres = [(embedding, title, synopsis) for embedding, (_, synopsis, title) in zip(embeddings, corpus)]
    
    # Sauvegarde du modèle dans un fichier pickled
    with open("../../models/sentence_similarity_model", "wb") as model_file:
        pickle.dump(model, model_file)
    
    # Sauvegarde de la liste dans un fichier pickled
    with open("../../embeddings/embeddings_corpus_movie", "wb") as embedding_corpus_file:
        pickle.dump(oeuvres, embedding_corpus_file)
    
    ####################################
    
    # # Requête de l'utilisateur
    # input = " ".join(sys.argv[1:])
    
    # # Recherche des oeuvres dont les synopsis sont les plus proches de la requête
    # results = get_similar_works(input, oeuvres=oeuvres, model=model)