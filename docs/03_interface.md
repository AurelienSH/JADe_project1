# :spider_web: Interface :spider_web:

:clapper: Synsearch a été construit à l'aide de FastAPI. 

## Getting started

```bash
git clone https://github.com/AurelienSH/JADe_project1
cd JADe_project1
pip install -U -r requirements.txt # Installation des dépendances

# Lancement de l'API
cd app/src
uvicorn main:app
```

- Interface graphique : <http://127.0.0.1:8000/front/index.html>
- Documentation interactive générée par FastAPI :
  - V1 : <http://127.0.0.1:8000/api/v1/docs>
  - V2 : <http://127.0.0.1:8000/api/v2/docs>
- Demo de la V2 avec le module Python `requests` : `JADe_project1/demo/demo_synsearch_requests` 

>[!note]
>Le démarrage de l'API peut prendre un peu de temps :
>
>- Chargement des modèles et des embeddings
>- Vérification de s'il faut faire le finetuning hebdomadaire
>- Et éventuellement ledit finetuning

## Architecture de l'API

Tous les fichiers relatifs au fonctionnement de l'API se trouve dans le dossier `JADe_project1/app`. 

```bash
app
├── embeddings  # Embeddings de notre corpus 
│   ├── embeddings_FT_corpus_movie  # Embeddings créé avec le dernier modèle finetuné
│   └── embeddings_corpus_movie  # Embeddings créé avec le modèle non-finetuné
├── models
│   ├── sentence_similarity_model  # Modèle gelé (V1)
│   └── sentence_similarity_model_FT  # Modèle finetuné (V2)
├── src
│   ├── scripts  # Scripts pour notre tâche de recherche de synopsis similaires
│   │   ├── finetune_first_model.py
│   │   ├── finetuning.py
│   │   ├── preprocessing.py
│   │   ├── similarity.py
│   │   └── utils.py  # Lancement du finetuning hebdomadaire
│   ├── database.db  # BDD des reviews utilisateurs 
│   ├── database.py  # Création de la BDD
│   ├── main.py
│   ├── models.py  # Définition des tables de la BDD et des colonnes
│   ├── schemas.py  # Modèles Pydantic pour la data validation
│   └── services.py  # Accéder à la BDD (CRUD)
├── static  # Fichiers static pour l'interface graphique
│   ├── LICENSE.txt
│   ├── README.txt
│   ├── assets
│   │   ├── css
│   │   ├── js  # thumbUp.js, submitSynopsis.js
│   │   ├── sass
│   │   └── webfonts
│   ├── images
│   └── index.html
└── templates  # Templates Jinja 
    └── result_table.html.jinja
```

### Déroulement du fonctionnement de l'API

L'API est lancée à partir de `app/src/main.py`. Lors du lancement, la BDD est créée (`app/src/database.py`) et les modèles et les embeddings du corpus sont chargés. Un finetuning hebdomadaire se fait automatiquement. 

A chaque lancement de l'API, il y a donc une vérification, grâce au script `app/src/scripts/utils.py` de si le finetuning est nécessaire. Si oui, il est lancé grâce au script `app/src/scripts/finetuning.py`. 

Lorsqu'une requête de recherche de films similaires est faite ([endpoint `/similar-works/`](03_interface.md#endpoint-similar-works)), le script `app/src/scripts/similarity.py` est appelé.

Lorsqu'une review est ajoutée ([endpoint `/reviews/`](03_interface.md#endpoint-reviews)), elle est ajoutée à la BDD grâce au script `app/src/services.py`. Ce dernier contient toutes les fonctions CRUD. 

Le script `app/src/schemas.py` contient la définition des modèles Pydantic pour la validation du format des données. Le script `app/src/models.py` quant à lui contient la définition des tables et des colonnes de la BDD. 

### Déroulement du fonctionnement de l'interface graphique

Dans l'interface graphique, quand l'utilisateur écrit un synopsis et envoie le formulaire, une requête POST est faite au endpoint `/similar-works/` de notre API grâce au script `app/static/assets/js/submitSynopsis.js`. Le résutat récupéré est ensuite écrit sous la forme d'un tableau à trois colonnes (titre de l'oeuvre, synopsis de l'oeuvre, avis) grâce au template Jinja `app/templates/result_table.html.jinja`. 

La troisième colonne "avis" contient deux boutons : un :+1: et un :-1:. Elle permet de prendre en compte l'avis de l'utilisateur dans notre système. Quand l'utilisateur clique sur un des boutons pour une oeuvre donnée, une requête POST au endpoint `/reviews/` est envoyée grâce au script `app/static/assets/js/thumbUp.js`.

## Fonctionnalités

### Endpoint `/similar-works/`

Ce endpoint permet d'obtenir les 5 oeuvres dont le synopsis est le plus similaire à un input. Pour en savoir plus sur comment cette similarité est calculée, se référer à la Section [Système](./02_systeme.md).

Schéma : 

```json
{
  "content": "I'm looking for a movie in which..."
}
```

Reponse :

```json
[ 
    {
        "title": "First Result",
        "content": "The synopsis of First Result"
    },
    {
        "title": "Second Result", 
        "content": "The synopsis of Second Result"
    },
    ...
]
```

Requête : 

```python
requests.post("http://127.0.0.1:8000/api/v2/similar-works/", 
                headers={"accept": "application/json", "Content-Type": "application/json"}, 
                json={"content": "I'm looking for a movie in which..."})
```

### Endpoint `/reviews/`

Ce endpoint permet de donner son avis sur un résultat. Cet avis est enregistré dans `JADe_project1/app/src/database.db` pour être plus tard utilisé pour le finetuning du modèle. 

Si on veut laisser un review *positive* (le résultat ressemble bien à la requête écrite), il faut que l'attribue `score` du schéma soit `pos`. Au contraire, si on veut laisser une review *négative* (le résultat ne ressemble pas à la requête écrite), `score` doit avoir la valeur `neg`

!>Si l'attribut `score` a une valeur autre que `pos` ou `neg`, une exception 400 est levée. 

Schéma : 

```json
{
  "title": "First Result",
  "synopsis": "The synopsis of First Result",
  "query": "I'm looking for a movie in which...",
  "score": "pos" // ou "neg"
}
```

Response : 

```json
{
  "title": "First Result",
  "synopsis": "The synopsis of First Result",
  "query": "I'm looking for a movie in which...",
  "score": "pos", 
  "id": 0  // Identifiant unique dans la BDD
}
```

Requête : 

```python
requests.post("http://127.0.0.1:8000/api/v2/reviews/", 
                headers={"accept": "application/json", "Content-Type": "application/json"}, 
                json={"title": "First Result", "synopsis": "The synopsis of First Result", "query": "I'm looking for a movie in which...", "score": "pos"})
```