####################################################################
#                                                                  # 
#                        IMPORTATION DES                           #
#                            MODULES                               #
#                                                                  #
####################################################################
 
import pydantic as _pydantic
from typing import List

####################################################################
#                                                                  # 
#                             QUERY                                #
#                                                                  #
####################################################################

class Query(_pydantic.BaseModel):
    """Schéma pydantic représentant une requête écrite par un utilisateur.

    Attributes:
        content (str): le contenu de la requête de l'utilisateur.
    """
    content: str

####################################################################
#                                                                  # 
#                             REVIEW                                #
#                                                                  #
####################################################################

class _ReviewBase(_pydantic.BaseModel):
    """Schéma pydantic pour la base d'une review dans la BDD.

    Attributes:
        title (str): le titre de l'oeuvre pour laquelle l'utilisateur a laissé une review
        synopsis (str): le synopsis de l'oeuvre pour laquelle l'utilisateur a laissé une review
        query (str): la requête écrite par l'utilisateur
        score (str): "pos" pour une review positive, "neg" pour une review négative
    """
    title: str
    synopsis: str
    query: str
    score: str
    
class ReviewAdd(_ReviewBase):
    """Schéma pydantic pour la création d'une review dans la BDD (hérite de `_ReviewBase`).
    
    Schéma à part même si pas d'attributs supplémentaires par rapport à la classe dont 
    il hérite parce qu'on voulait bien séparer. 

    Attributes:
        title (str): le titre de l'oeuvre pour laquelle l'utilisateur a laissé une review
        synopsis (str): le synopsis de l'oeuvre pour laquelle l'utilisateur a laissé une review
        query (str): la requête écrite par l'utilisateur
        score (str): "pos" pour une review positive, "neg" pour une review négative
    """
    pass
      
class DBReview(_ReviewBase):
    """Schéma représentant une review effectivement créée dans la BDD.

    Attributes:
        id (int): l'identifiant unique de la review
        title (str): le titre de l'oeuvre pour laquelle l'utilisateur a laissé une review
        synopsis (str): le synopsis de l'oeuvre pour laquelle l'utilisateur a laissé une review
        query (str): la requête écrite par l'utilisateur
        score (str): "pos" pour une review positive, "neg" pour une review négative
    """
    id: int
    
    class Config:
        orm_mode = True
    