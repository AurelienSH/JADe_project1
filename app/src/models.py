########## IMPORTATION ##########
 
import database as _database
import sqlalchemy as _sql

#################################
    
class Review(_database.Base):
    """
    Représente une review dans la BDD
    
    Attributes:
        - id (int) : La clé primaire du film
        - title (str) : Le titre de l'oeuvre pour laquelle l'utilisateur a donné une review. Ne peut pas être vide.
        - synopsis (str) : Le synopsis de l'oeuvre pour laquelle l'utilisateur a donné une review.
        - pos_query (list) : Une liste contenant toutes les queries qui ont amené l'utilisateur a laissé une review positive pour cette oeuvre
        - neg_query (list) : Une liste contenant toutes les queries qui ont amené l'utilisateur a laissé une review négative pour cette oeuvre
    """
    
    # Nom de la table
    __tablename__ = "movie_review"
    
    # Définition des colonnes
    
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)
    title = _sql.Column(_sql.String, nullable = False, index = True)
    synopsis = _sql.Column(_sql.String, nullable = False, index = True)
    query = _sql.Column(_sql.String) # Liste queries positives
    score = _sql.Column(_sql.String) # Liste queries négatives