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
):

    db_review = _models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
   
    return db_review

def get_data_for_FT(db: _orm.Session) -> List[InputExample]:
    
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