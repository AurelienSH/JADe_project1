##############################################################
#                                                            #
#                     IMPORTATION DES MODULES                #
#                                                            #
##############################################################

from typing import List, Tuple
import pickle # Sauvegarde des embeddings
from preprocessing import read_corpus, make_embeddings_corpus

# Transformers
from sentence_transformers import SentenceTransformer

# Calcul de similarité
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances
    

##############################################################
#                                                            #
#                    CALCUL DE SIMILARITE                    #
#                                                            #
##############################################################

def get_similar_works(user_input: str, oeuvres: List[Tuple], model: SentenceTransformer, k: int=5, distance_type = "cos"):
    
    # Vectorization de la requête de l'utilisateur avec le modèle
    input_encoded = model.encode(user_input)
    
    similars = []
    
    # Calcul de la distance cosinus entre chaque oeuvre 
    # de la liste d'oeuvre et la requête de l'utilisateur
    for (embedding_oeuvre, title, synopsis) in oeuvres:
        
        # Création résultat sous la forme d'un tuple (distance, title, synopsis)
        
        if distance_type == "cos": # Distance cosinus
            result = (cosine_distances([embedding_oeuvre], [input_encoded]), title, synopsis)
            
        elif distance_type == "eucl": # Distance euclidienne
            result = (euclidean_distances([embedding_oeuvre], [input_encoded]), title, synopsis)
        
        else:
            print("Valeurs de distance_type acceptées : 'cos' ou 'eucl'")
            return
        
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
    model = SentenceTransformer(model_name_or_path='sentence-transformers/all-MiniLM-L6-v2')

    # Liste contenant toutes les oeuvres sous la forme d'un tuple (embedding, tile, synopsis)
    oeuvres = make_embeddings_corpus(corpus=corpus, model=model)
    
    # Sauvegarde du modèle
    model.save("../../models/sentence_similarity_model")
    
    # Sauvegarde des embeddings dans un fichier pickled
    with open("../../embeddings/embeddings_corpus_movie", "wb") as embedding_corpus_file:
        pickle.dump(oeuvres, embedding_corpus_file)