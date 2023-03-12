########## IMPORTATION ##########

import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import fastapi as _fastapi
from sqlalchemy import and_

from typing import List

from sentence_transformers import InputExample

########## CREATION DATABASE + SESSION ##########

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

################################# CRUD ###################################

# def create_synopsis(db: _orm.Session, synopsis: _schemas.SynopsisCreate) -> _schemas.DBSynopsis:
#     db_synopsis = _models.Synopsis(**synopsis.dict())
#     db.add(db_synopsis)
#     db.commit()
#     db.refresh(db_synopsis)
#     return db_synopsis

# def create_query(
#     db: _orm.Session, 
#     query: _schemas.QueryCreate
# ) -> _schemas.Query:
#     db_query = _models.Query(**query.dict())
#     db.add(db_query)
#     db.commit()
#     db.refresh(db_query)
#     return db_query

# def find_synopsis_containing_word(
#     db: _orm.Session,
#     input: str):
    
#     return db.query(_models.Synopsis.title, _models.Synopsis.type, _models.Synopsis.date_published, _models.Synopsis.content).where(_models.Synopsis.content.contains(input)).limit(5).all()

# def delete_synopsis(
#     synopsis_to_delete: _schemas.SynopsisCreate,
#     db: _orm.Session,
# ):
    
#     # Sélection du synopsis à supprimer de la BDD
#     db_synopsis_to_delete = db.query(_models.Synopsis).where(
#         and_(_models.Synopsis.title == synopsis_to_delete.title,
#         _models.Synopsis.date_published == synopsis_to_delete.date_published,
#         _models.Synopsis.type == synopsis_to_delete.type, 
#         _models.Synopsis.content == synopsis_to_delete.content)).first()
    
#     # Vérification qu'il se trouve bien dans la BDD
#     if db_synopsis_to_delete:
#         db.delete(db_synopsis_to_delete)
#         db.commit()
#     else:
#         raise _fastapi.HTTPException(status_code=404, detail="Synopsis not found")
    
#     return {
#         "message": f"Suppresion du synopsis effectuée."
#     }
    
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