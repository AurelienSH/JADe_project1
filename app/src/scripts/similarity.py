##############################################################
#                                                            #
#                     IMPORTATION DES MODULES                #
#                                                            #
##############################################################

from typing import List, Tuple, Dict  # Typage des fonctions
import pickle  # Sauvegarde des embeddings

# Transformers
from sentence_transformers import SentenceTransformer

# Calcul de similarité
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances


##############################################################
#                                                            #
#                    CALCUL DE SIMILARITE                    #
#                                                            #
##############################################################

def get_similar_works(user_input: str,
                      oeuvres: List[Tuple],
                      model: SentenceTransformer,
                      k: int = 5,
                      distance_type="cos"
                      ) -> List[Dict[str, str] | None]:
    """Obtenir les oeuvres dont le synopsis est similaire à la requête écrite
    par l'utilisateur.
    
    La requête écrite par l'utilisateur (`user_input`) est vectorisée à l'aide du même `model` utilisé
    pour la vectorisation du corpus. La similarité est calculée avec la distance cosinus (`distance_type = "cos"`)
    ou euclidienne (`distance_type = "eucl"`) entre l'`user_input` vectorisé et les embeddings
    des synopsis du corpus se trouvant dans `oeuvres`. Elle renvoie les `k` oeuvres plus similaires, dont les `k`
    oeuvres pour laquelle la distance est la plus basse. 

    Args:
        user_input (str): la requête écrite par l'utilisateur
        oeuvres (List[Tuple]): le corpus sous la forme d'une liste de tuples (embedding_synopsis, title, synopsis)
        model (SentenceTransformer): le modèle à utiliser pour créer les embeddings
        k (int, optional): le nombre d'oeuvres similaires à renvoyer. Par défaut 5.
        distance_type (str, optional): la distance à utiliser. Par "cos" pour la distance cosinus. 
            Autre possibilité : "eucl" pour la distance euclidienne.

    Returns:
        List[Dict[str, str]]: les oeuvres les plus similaires sous la forme d'une liste de
            dictionnaires [{"title": title, "content": synopsis}]
        None: si la valeur de `distance_type` n'est pas valide
    """

    # Vectorization de la requête de l'utilisateur avec le modèle
    input_encoded = model.encode(user_input)

    results = []

    # Calcul de la distance cosinus entre chaque oeuvre 
    # de la liste d'oeuvre et la requête de l'utilisateur
    for (embedding_oeuvre, title, synopsis) in oeuvres:

        # Création résultat sous la forme d'un tuple (distance, title, synopsis)

        # Distance cosinus
        if distance_type == "cos":
            result = (cosine_distances([embedding_oeuvre], [input_encoded]), title, synopsis)

        # Distance euclidienne
        elif distance_type == "eucl":
            result = (euclidean_distances([embedding_oeuvre], [input_encoded]), title, synopsis)

        else:
            print("Valeurs de distance_type acceptées : 'cos' ou 'eucl'")
            return None  # type: ignore

        # Stockage des résultats dans une liste
        results.append(result)

    # Triage des résultats selon la distance par ordre croissant
    # Pour obtenir les oeuvres les plus proches 
    sorted_results = sorted(results, key=lambda x: x[0])

    return [{"title": title, "content": synopsis} for _, title, synopsis in sorted_results[:k]]
