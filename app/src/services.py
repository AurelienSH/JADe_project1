########## IMPORTATION ##########

import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas

from typing import Dict, List

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
    
    return db.query(_models.Synopsis.title, _models.Synopsis.date_published).where(_models.Synopsis.content.contains(input)).all()
