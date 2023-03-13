####################################################################
#                                                                  # 
#                        IMPORTATION DES                           #
#                            MODULES                               #
#                                                                  #
####################################################################

# Interface graphique et API
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import fastapi as _fastapi

# Database
import sqlalchemy.orm as _orm
import schemas as _schemas
import services as _services

# Similarité 
import scripts.similarity as _similarity

# Entraînement du modèle
import pickle # Sauvegarde des embeddings
from scripts.preprocessing import make_embeddings_corpus, read_corpus
from sentence_transformers import SentenceTransformer, SentencesDataset, InputExample, losses
from torch.utils.data import DataLoader
from scripts.finetuning import finetune_model


####################################################################
#                                                                  # 
#                              API ET BDD                          #
#                                 SETUP                            #
#                                                                  #
####################################################################

# Versions de notre API
app = _fastapi.FastAPI()
v1 = _fastapi.FastAPI()
v2 = _fastapi.FastAPI()

app.mount("/api/v1", v1)
app.mount("/api/v2", v2)

# Création de la database
_services.create_database()

# Autorisation des requêtes POST
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
)

# Fichiers Static
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

# Récupération du modèle non fine-tuné
model = SentenceTransformer(f"{models_path}/sentence_similarity_model")

# Récupération du modèle fine-tuné
model_FT = SentenceTransformer(f"{models_path}/sentence_similarity_model_FT")

# Récupération des embeddings du corpus pour la V1
with open(f"{embeddings_path}/embeddings_corpus_movie", "rb") as file:
    embeddings_corpus_movie = pickle.load(file)
    
# Récupération des embeddings du corpus pour la V2
with open(f"{embeddings_path}/embeddings_FT_corpus_movie", "rb") as file:
    embeddings_FT_corpus_movie = pickle.load(file)

# Finetuning hebdomadaire
finetune_model(db = _fastapi.Depends(_services.get_db), model=model_FT, model_path = models_path)


####################################################################
#                                                                  #
#              VERSION 1 : SENTENCE SIMILARITY                     #
#                                                                  #
####################################################################

@v1.post("/similar-works/")
async def get_similar_works(
    request: _fastapi.Request, 
    input: _schemas.Query,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    # Recherche des oeuvres les plus similaires avec le modèle non fine-tuné
    similars = _similarity.get_similar_works(user_input=input.content,
                                             oeuvres=embeddings_corpus_movie,
                                             model=model)
    
    accept_header = request.headers.get('Accept')
    
    # Résultat pour l'interface graphique
    if "text/html" == accept_header:       
        return templates.TemplateResponse(
            "result_table.html.jinja", 
            {
            "request": request,
            "input_user": input.content, # le synopsis écrit par l'utilisateur
            "similars": similars,
            }
        )
        
    # Résultat pour une requête depuis le terminal
    elif "application/json" == accept_header:       
        return similars
    
    
####################################################################
#                                                                  #
#            VERSION 2 : SENTENCE SIMILARITY FINE-TUNE             #
#                                                                  #
####################################################################

@v2.post("/similar-works/")
async def get_similar_works_FT(
    request: _fastapi.Request, 
    input: _schemas.Query,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    # Recherche des oeuvres les plus similaires avec le modèle fine-tuné
    similars = _similarity.get_similar_works(user_input = input.content, 
                                           model=model_FT,
                                           oeuvres=embeddings_FT_corpus_movie
                                           )
    
    accept_header = request.headers.get('Accept')
    
    # Résultat pour l'interface graphique
    if "text/html" == accept_header:        
        return templates.TemplateResponse(
            "result_table.html.jinja", 
            {
            "request": request,
            "input_user": input.content, # le synopsis écrit par l'utilisateur
            "similars": similars,
            }
        )
        
    # Résultat pour une requête depuis le terminal
    elif "application/json" == accept_header:      
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