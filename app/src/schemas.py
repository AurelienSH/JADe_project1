########## IMPORTATION ##########
 
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import pydantic as _pydantic

########## QUERIES ##########

class QueryCreate(_pydantic.BaseModel):
    synopsis: str
    
# class QueryCreate(_QueryBase):
#     pass

class Query(QueryCreate):
    id: int
    
    class Config:
        orm_mode = True

########## SYNOPSIS ##########

class _SynopsisBase(_pydantic.BaseModel):
    title: str
    date_published: int
    type: str
    content: str
    
class SynopsisCreate(_SynopsisBase):
    pass
    
class DBSynopsis(_SynopsisBase):
    id: int
    
    class Config:
        orm_mode = True
    