########## IMPORTATION ##########

import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import fastapi as _fastapi
from sqlalchemy import and_

from typing import List, Tuple
import pickle

import scripts.sentence_similarity as _sentence_similarity

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
    
def create_new_review(
    db: _orm.Session,
    new_review: _schemas.ReviewCreate
):
    
    # Recherche du film dans la BDD des reviews
    existing_review = db.query(_models.Review).filter(_models.Review.title.ilike(new_review.title)).first()
    
    if existing_review: # Film a déjà eu des reviews
        return existing_review
    
    else: # Première review pour ce film donc ajout dans la BDD
        db_review = _models.Review(new_review)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
    return db_review
    
def add_movie_review(
    db: _orm.Session,
    review: _schemas.ReviewAdd
):
    
    # Vérification de la présence du film dans la BDD
    # Sinon ajout dans la BDD 
    db_review = create_new_review(db=db, new_review=_schemas.ReviewCreate(**review.dict()))
    
    if review.value == "pos": # Review positive
        db_review.pos_query.append(review.query)
    
    elif review.value == "neg": # Review négative
        db_review.neg_query.append(review.query)
        
    print("#####################################################")
    print(db_review.pos_query)
    print(db_review.neg_query)
    print("#####################################################")
        
    return db_review
        
    
####################################################################################

def cosine_similarity(user_input: str, oeuvres: List[Tuple], model, k: int = 5):
    
    return _sentence_similarity.get_similar_works(user_input=user_input, oeuvres=oeuvres, model=model) # type: ignore
    