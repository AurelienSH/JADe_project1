########## IMPORTATION ##########
 
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import pydantic as _pydantic

from typing import List

########## MOVIE REVIEW ##########

class _ReviewBase(_pydantic.BaseModel):
    title: str
    synopsis: str
    pos_query: List[str] = []    
    neg_query: List[str] = []
    
class ReviewCreate(_ReviewBase):
    pass
    
class DBReview(_ReviewBase):
    id: int
    
    class Config:
        orm_mode = True
    