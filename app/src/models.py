########## IMPORTATION ##########
 
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import database as _database
import sqlalchemy as _sql

#################################

class Query(_database.Base):
    """
    Représente une requête dans la base de données, 
    quand un utilisateur cherche une oeuvre similaire
    au synopsis qu'il a rentré.
    
    Attributes:
        - id (int) : La clé primaire de la requête.
        - synopsis (str) : Le contenu de la requête.
    """
    
    # Nom de la table
    __tablename__ = "queries"
    
    # Définition des colonnes
    
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)
    synopsis = _sql.Column(_sql.String)
    
class Synopsis(_database.Base):
    """
    Représente un Synopsis dans la base de données.
    
    Attributes:
        - id (int) : La clé primaire du synopsis.
        - title (str) : Le titre de l'oeuvre correspond à ce synopsis. Ne peut pas être vide.
        - date_published (int) : La date de publication de l'oeuvre correspond à ce synopsis.
        - type (str) : Le type de l'oeuvre correspond à ce synopsis (film, série, livre...)
    """
    
    # Nom de la table
    __tablename__ = "synopsis"
    
    # Définition des colonnes
    
    id = _sql.Column(_sql.Integer, primary_key = True, index = True)
    title = _sql.Column(_sql.String, nullable = False, index = True)
    date_published = _sql.Column(_sql.Integer, index = True)
    type = _sql.Column(_sql.String)
    content = _sql.Column(_sql.String)