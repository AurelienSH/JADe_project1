########## IMPORTATION ##########
 
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import pydantic as _pydantic

from typing import List

############# QUERIES ############

class Query(_pydantic.BaseModel):
    content: str

########## MOVIE REVIEW ##########

class _ReviewBase(_pydantic.BaseModel):
    title: str
    synopsis: str
    query: str
    score: str
    
class ReviewAdd(_ReviewBase):
    pass
      
class DBReview(_ReviewBase):
    id: int
    
    class Config:
        orm_mode = True
    