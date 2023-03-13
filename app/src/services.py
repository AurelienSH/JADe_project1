####################################################################
#                                                                  # 
#                        IMPORTATION DES                           #
#                            MODULES                               #
#                                                                  #
####################################################################

import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import fastapi as _fastapi
from sqlalchemy import and_

from typing import List

from sentence_transformers import InputExample


####################################################################
#                                                                  # 
#                        CREATION DATABASE                         #
#                            ET SESSION                            #
#                                                                  #
####################################################################

def create_database():
    """
    Crée toutes les tables dans la base de données.
    """
    return _database.Base.metadata.create_all(bind = _database.engine)

def get_db() -> _orm.Session: # type: ignore    
    """
    Cette fonction retourne une session active pour accéder à la BDD.
    La session sera fermée automatiquement.
    """
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


####################################################################
#                                                                  # 
#                              CRUD                                #
#                                                                  #
####################################################################

def add_movie_review(
    db: _orm.Session,
    review: _schemas.ReviewAdd
) -> _schemas.DBReview:
    """Ajouter une review à la BDD.
    
    Cette fonction permet, à partir d'un objet `ReviewAdd`, d'ajouter une
    review à la table `movie_review` de la BDD.

    Args:
        db (_orm.Session): Une session permettant d'accéder à la BDD
        review (_schemas.ReviewAdd): la review à ajouter à la BDD

    Returns:
        _schemas.DBReview: la review effectivement ajoutée à la BDD
    """

    # Création de l'objet Review correspondant à une entrée de la table `movie_review`
    db_review = _models.Review(**review.dict())
    
    # Ajout de l'entrée à la table
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
   
    return db_review

def get_data_for_FT(db: _orm.Session) -> List[InputExample]:
    """Permet d'obtenir les données nécessaires pour le finetuning du modèle.
    
    Cette fonction renvoie toutes les données d'une `db` sous la forme nécessaire
    pour le finetuning de notre modèle. C'est-à-dire sous une liste de 
    `InputExample(texts=[synopsis, query], label)`. 
    
    Si la review est négative, on attribue le label 1.5 (distance très grande => synopsis
    et query ne sont pas similaires), si la review est positive 0.2 (distance très petite => 
    synopsis et query sont similaires).

    Args:
        db (_orm.Session): la session permettant d'accéder à la BDD

    Returns:
        List[InputExample]: les données d'entraînement dans le bon format
    """
    
    train_examples = []
    
    # Dico pour transformer les scores écrits en string en des distances
    score2label = {
        "neg": 1.5,
        "pos": 0.2
    }
    
    # Création des objet InputExample servant à entraîner le modèle à partir des données de la BDD
    for synopsis, query, score in db.query(_models.Review.synopsis, _models.Review.query, _models.Review.score).all():
        train_examples.append(
            InputExample(texts=[synopsis, query],
                         label=score2label[score])
        )
        
    return train_examples