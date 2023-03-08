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
    
class ReviewAdd(_ReviewBase):
    query: str
    value: str
    
class ReviewCreate(_ReviewBase):
    pass
      
class DBReview(_ReviewBase):
    id: int
    pos_query: List[str]
    neg_query: List[str]
    
    @classmethod
    def create(cls, **data):
        return cls(
            pos_query=data.get('pos_query', []),
            neg_query=data.get('neg_query', []),
            **data,
        )
    
    class Config:
        orm_mode = True
    