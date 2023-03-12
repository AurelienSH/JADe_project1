####################################################################
#                                                                  # 
#                        IMPORTATION DES                           #
#                            MODULES                               #
#                                                                  #
####################################################################

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import sqlalchemy.orm as _orm
import fastapi as _fastapi
import schemas as _schemas
import services as _services

import pickle

import scripts.similarity as _similarity

from sentence_transformers import SentenceTransformer, SentencesDataset, InputExample, losses
from torch.utils.data import DataLoader
from scripts.preprocessing import make_embeddings_corpus, read_corpus

####################################################################
#                                                                  # 
#                              API ET BDD                          #
#                                 SETUP                            #
#                                                                  #
####################################################################

# Versions de notre API
app = FastAPI()
v0 = FastAPI()
v1 = FastAPI()
v2 = FastAPI()

app.mount("/api/v0", v0)
app.mount("/api/v1", v1)
app.mount("/api/v2", v2)

# Création de la database
_services.create_database()


# Autorisation des requêtes POST et DELETE
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST", "DELETE"],
)

# Fichier Static
app.mount("/front", StaticFiles(directory="../static"), name="front")

templates = Jinja2Templates(directory="../templates")

####################################################################
#                                                                  # 
#                       CHARGEMENT DES MODELES                     #
#                         ET DES EMBEDDINGS                        #
#                                                                  #
####################################################################

models_path = "../models"
embeddings_path = "../embeddings"

# Récupération du modèle depuis le fichier pickled (pour la V1)
with open(f"{models_path}/sentence_similarity_model", "rb") as file:
    model = pickle.load(file)

# Récupération du modèle fine-tuné
model_FT = SentenceTransformer(f"{models_path}/sentence_similarity_model_FT")

# Récupération des embeddings du corpus pour la V1
with open(f"{embeddings_path}/embeddings_corpus_movie", "rb") as file:
    embeddings_corpus_movie = pickle.load(file)
    
# Récupération des embeddings du corpus pour la V2
with open(f"{embeddings_path}/embeddings_FT_corpus_movie", "rb") as file:
    embeddings_FT_corpus_movie = pickle.load(file)

####################################################################
#                                                                  #
#                  VERSION 0 : Renvoyer oeuvres                    #
#                  qui contiennent le mot de la requête            #
#                     dans leur synopsis                           #
#                                                                  #
####################################################################


# @v0.post("/similar-works/")
# async def find_synopsis_containing_word(
#     request: Request, 
#     input: _schemas.Query,
#     db: _orm.Session = _fastapi.Depends(_services.get_db)):
#     """Récupère la requête envoyée par le formulaire,
#     le réécrit en dessous du formulaire et renvoie toutes les oeuvres
#     qui contiennent les mots de la requête sous la forme d'un tableau
#     avec : le nom de l'oeuvre, la date de publication, le type d'oeuvre
#     (film, série...). 
    
#     Utilise le template Jinja `submit_success.html.jinja` pour écrire
#     le tableau des résultats.
#     """
    
#     # Enregistrement de la requête dans la BDD
#     # _services.create_query(db=db, query=input)

#     # Liste des oeuvres similaires avec quelques métadonnées
#     similars = _services.find_synopsis_containing_word(db=db, input=input.content)
    
#     accept_header = request.headers.get('Accept')
    
#     # Résultat pour l'interface graphique
#     if "text/html" in accept_header: # type: ignore        
#         return templates.TemplateResponse(
#             "result_table.html.jinja", 
#             {
#             "request": request,
#             "input_user": input.synopsis, # le synopsis écrit par l'utilisateur
#             "similars": similars,
#             }
#         )
        
#     # Résultat pour une requête depuis le terminal
#     elif "application/json" in accept_header: # type: ignore        
#         return similars
    
# @v0.post("/synopsis/", response_model = _schemas.DBSynopsis)
# def create_synopsis(
#     synopsis: _schemas.SynopsisCreate, 
#     db: _orm.Session = _fastapi.Depends(_services.get_db)
#     ) -> _schemas.DBSynopsis:
#     """Ajoute le synopsis dans la table "synopsis" 
#     de notre base de données.

#     Args:
    
#     - `synopsis` (`_schemas.SynopsisCreate`): Le synopsis qu'on veut ajouter à note database (le titre de l'oeuvre, la date de publication, le type de l'oeuvre et le contenu du synopsis)
#     - `db` (`_orm.Session`, optional): la session pour accéder à la database. Par défaut : `_fastapi.Depends(_services.get_db)`.

#     Returns:
    
#     - (`_schemas.DBSynopsis`): Le synopsis créé dans la database, avec un `id` unique assigné automatiquement par la database.
#     """
#     return _services.create_synopsis(db = db, synopsis = synopsis)

# @v0.delete("/synopsis/")
# def delete_synopsis(
#     synopsis_to_delete: _schemas.SynopsisCreate,
#     db: _orm.Session=_fastapi.Depends(_services.get_db)
# ):
#     """Supprimer un synopsis de la BDD."""
#     return _services.delete_synopsis(synopsis_to_delete=synopsis_to_delete, db=db)
    
    

####################################################################
#                                                                  #
#              VERSION 1 : SENTENCE SIMILARITY                     #
#                                                                  #
####################################################################

@v1.post("/similar-works/")
async def get_similar_works(
    request: Request, 
    input: _schemas.Query,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    # Recherche des oeuvres les plus similaires avec le modèle non fine-tuné
    similars = _similarity.get_similar_works(user_input=input.content,
                                             oeuvres=embeddings_corpus_movie,
                                             model=model)
    
    accept_header = request.headers.get('Accept')
    
    # Résultat pour l'interface graphique
    if "text/html" in accept_header: # type: ignore        
        return templates.TemplateResponse(
            "result_table.html.jinja", 
            {
            "request": request,
            "input_user": input.content, # le synopsis écrit par l'utilisateur
            "similars": similars,
            }
        )
        
    # Résultat pour une requête depuis le terminal
    elif "application/json" in accept_header: # type: ignore        
        return similars
    
    
####################################################################
#                                                                  #                           #
#            VERSION 2 : SENTENCE SIMILARITY FINE-TUNE             #
#                                                                  #                            #
####################################################################

@v2.post("/similar-works/")
async def get_similar_works_FT(
    request: Request, 
    input: _schemas.Query,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    # Recherche des oeuvres les plus similaires avec le modèle fine-tuné
    similars = _similarity.get_similar_works(user_input = input.content, 
                                           model=model_FT,
                                           oeuvres=embeddings_FT_corpus_movie
                                           )
    
    accept_header = request.headers.get('Accept')
    
    # Résultat pour l'interface graphique
    if "text/html" in accept_header: # type: ignore        
        return templates.TemplateResponse(
            "result_table.html.jinja", 
            {
            "request": request,
            "input_user": input.content, # le synopsis écrit par l'utilisateur
            "similars": similars,
            }
        )
        
    # Résultat pour une requête depuis le terminal
    elif "application/json" in accept_header: # type: ignore        
        return similars
    
@v2.post("/reviews/", response_model=_schemas.DBReview)
async def add_review(
    review: _schemas.ReviewAdd,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    
    # Ajout de la review dans la BDD
    new_review = _services.add_movie_review(
        db=db,
        review=review
    )
    
    return new_review

@v2.get("/test/")
def finetune_model(
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    
    # Récupération des données de la BDD
    # Et mise en forme dans le bon format pour l'entraînement
    train_examples = _services.get_data_for_FT(db=db)
    train_dataset = SentencesDataset(train_examples, model)
    
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=16)
    train_loss = losses.CosineSimilarityLoss(model_FT)
    
    # Entrainement du modèle
    model_FT.fit(train_objectives=[(train_dataloader, train_loss)],
                 epochs=3,
                 warmup_steps=100)
    
    # Sauvegarde du modèle
    model_FT.save(f"{models_path}/sentence_similarity_model_FT")
    
    # Recréation des embeddings avec le nouveau modèle fine-tuné sur les reviews
    corpus = read_corpus("../../Data/movie_synopsis.csv")    
    embeddings_FT_corpus_movie = make_embeddings_corpus(corpus=corpus, model=model_FT)
    
    # Sauvegarde des embeddings
    with open("../embeddings/embeddings_FT_corpus_movie", "wb") as embeddings_file:
        pickle.dump(embeddings_FT_corpus_movie, file=embeddings_file)
    
    return {
        "message": "modèle fine-tuné"
    }