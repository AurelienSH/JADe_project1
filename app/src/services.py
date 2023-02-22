########## IMPORTATION ##########

import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import fastapi as _fastapi

from typing import Dict, List

from sqlalchemy import and_

########## CREATION DATABASE + SESSION ##########

def create_database():
    """
    Crée toutes les tables dans la base de données.
    """
    return _database.Base.metadata.create_all(bind = _database.engine)

def get_db() -> _orm.Session:
    """
    Cette fonction retourne une session active pour accéder à la BDD.
    La session sera fermée automatiquement.
    """
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
################## CRUD ###################

def create_synopsis(db: _orm.Session, synopsis: _schemas.SynopsisCreate) -> _schemas.DBSynopsis:
    db_synopsis = _models.Synopsis(**synopsis.dict())
    db.add(db_synopsis)
    db.commit()
    db.refresh(db_synopsis)
    return db_synopsis

def create_query(
    db: _orm.Session, 
    query: _schemas.QueryCreate
) -> _schemas.Query:
    db_query = _models.Query(**query.dict())
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

def find_similar(
    db: _orm.Session,
    input: str):
    
    return db.query(_models.Synopsis.title, _models.Synopsis.type, _models.Synopsis.date_published, _models.Synopsis.content).where(_models.Synopsis.content.contains(input)).limit(5).all()

def delete_synopsis(
    synopsis_to_delete: _schemas.SynopsisCreate,
    db: _orm.Session,
):
    
    # Sélection du synopsis à supprimer de la BDD
    db_synopsis_to_delete = db.query(_models.Synopsis).where(
        and_(_models.Synopsis.title == synopsis_to_delete.title,
        _models.Synopsis.date_published == synopsis_to_delete.date_published,
        _models.Synopsis.type == synopsis_to_delete.type, 
        _models.Synopsis.content == synopsis_to_delete.content)).first()
    
    # Vérification qu'il se trouve bien dans la BDD
    if db_synopsis_to_delete:
        db.delete(db_synopsis_to_delete)
        db.commit()
    else:
        raise _fastapi.HTTPException(status_code=404, detail="Synopsis not found")
    
    return {
        "message": f"Suppresion du synopsis effectuée."
    }