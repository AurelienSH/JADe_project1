from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import sqlalchemy.orm as _orm
import fastapi as _fastapi
import schemas as _schemas
import services as _services

########## BROUILLON ##########

# env = Environment(
#     loader=FileSystemLoader("examples/templates"),
#     autoescape=False,
# )

# @app.get("/en")
# async def root_en():
#     return {"message": "Hello World"}


# @app.get("/fr")
# async def root_fr():
#     return {"message": "Wesh les individus"}

###############################

app = FastAPI()
v1 = FastAPI()
v2 = FastAPI()

# Création de la database
_services.create_database()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST", "DELETE"],
)

app.mount("/front", StaticFiles(directory="../static"), name="front")
app.mount("/api/v1", v1)
app.mount("/api/v2", v2)

templates = Jinja2Templates(directory="../templates")


################################################################################################
#                                                                                              #
#                                  VERSION 1 : SIMILARITE BASIQUE                              #
#                                                                                              #
################################################################################################


@v1.post("/similar-works/")
async def get_similar_works(
    request: Request, 
    input: _schemas.QueryCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """Récupère la requête envoyée par le formulaire,
    le réécrit en dessous du formulaire et renvoie toutes les oeuvres
    qui contiennent les mots de la requête sous la forme d'un tableau
    avec : le nom de l'oeuvre, la date de publication, le type d'oeuvre
    (film, série...). 
    
    Utilise le template Jinja `submit_success.html.jinja` pour écrire
    le tableau des résultats.
    """
    
    # Enregistrement de la requête dans la BDD
    # _services.create_query(db=db, query=input)

    # Liste des oeuvres similaires avec quelques métadonnées
    similars = _services.find_similar(db=db, input=input.synopsis)
    
    accept_header = request.headers.get('Accept')
    
    # Résultat pour l'interface graphique
    if "text/html" in accept_header: # type: ignore        
        return templates.TemplateResponse(
            "result_table.html.jinja", 
            {
            "request": request,
            "input_user": input.synopsis, # le synopsis écrit par l'utilisateur
            "similars": similars,
            }
        )
        
    # Résultat pour une requête depuis le terminal
    elif "application/json" in accept_header: # type: ignore        
        return similars
    
@v1.post("/synopsis/", response_model = _schemas.DBSynopsis)
def create_synopsis(
    synopsis: _schemas.SynopsisCreate, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)
    ) -> _schemas.DBSynopsis:
    """Ajoute le synopsis dans la table "synopsis" 
    de notre base de données.

    Args:
    
    - `synopsis` (`_schemas.SynopsisCreate`): Le synopsis qu'on veut ajouter à note database (le titre de l'oeuvre, la date de publication, le type de l'oeuvre et le contenu du synopsis)
    - `db` (`_orm.Session`, optional): la session pour accéder à la database. Par défaut : `_fastapi.Depends(_services.get_db)`.

    Returns:
    
    - (`_schemas.DBSynopsis`): Le synopsis créé dans la database, avec un `id` unique assigné automatiquement par la database.
    """
    return _services.create_synopsis(db = db, synopsis = synopsis)

@v1.delete("/synopsis/")
def delete_synopsis(
    synopsis_to_delete: _schemas.SynopsisCreate,
    db: _orm.Session=_fastapi.Depends(_services.get_db)
):
    """Supprimer un synopsis de la BDD."""
    return _services.delete_synopsis(synopsis_to_delete=synopsis_to_delete, db=db)
    
    

################################################################################################
#                                                                                              #
#                                  VERSION 2 : FINE-TUNING                                     #
#                                                                                              #
################################################################################################

@v2.post("/similar-works/")
async def get_similar_works_FT(
    request: Request, 
    input: _schemas.QueryCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return {"content": "prout"}