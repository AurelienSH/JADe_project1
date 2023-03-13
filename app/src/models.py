####################################################################
#                                                                  # 
#                        IMPORTATION DES                           #
#                            MODULES                               #
#                                                                  #
####################################################################
 
import database as _database
import sqlalchemy as _sql

####################################################################
    
class Review(_database.Base):
    """
    Représente une review dans la BDD
    
    Attributes:
        - id (int) : La clé primaire de la review
        - title (str) : Le titre de l'oeuvre pour laquelle l'utilisateur a donné une review. Ne peut pas être vide.
        - synopsis (str) : Le synopsis de l'oeuvre pour laquelle l'utilisateur a donné une review.
        - query (str) : La requête écrite par l'utilisateur
        - score (str) : "pos" pour une review positive, "neg" pour une review négative
    """
    
    # Nom de la table
    __tablename__ = "movie_review"
    
    # Définition des colonnes
    
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)
    title = _sql.Column(_sql.String, nullable = False, index = True)
    synopsis = _sql.Column(_sql.String, nullable = False, index = True)
    query = _sql.Column(_sql.String) # Requête écrite par l'utilisateur
    score = _sql.Column(_sql.String) # "pos" pour une review positive, "neg" pour une review négative