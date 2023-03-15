# PROJET API : trouver les oeuvres similaires

## :brain: Brainstorming :brain:

:::info
Cette section est le brainstorming qu'on a fait au tout début.
:::

Idée générale : Trouver oeuvre qui est la plus proche du résumé fourni par l'utilisateur

- on peut déjà commencer par un truc sans apprentissage
	- créer une baseline avec glove/word2vec
	- similarité cosinus
- récupérer des embeddings de résumés : doc2vec
- classifieur neuronal
- fine-tuner BERT
- évaluation : satisfaction utilisateur
- prendre en compte des tags/keywords ?

## :book: Cahier des charges :book:

:::info
Cette section sert à décrire les tâches qu'on doit faire.

On peut cocher au fur et à mesure les choses qu'on a faites et rajouter des tâches.
:::

### Den

- [ ] Faire des similarités basiques
    - Vectorisation avec word2vec/GloVe de la requête d'un utilisateur + similarité cosinus avec un synopsis d'un livre
    - FastText ?
- [ ] API : 2 gros pôles
	- [ ] faire l'API
	    - [x] Mettre en place une BDD fictive pour pouvoir tester si le lien entre le front et l'API/BDD fonctionne
		- [x] Faire en sorte qu'on puisse mettre un :-1:  ou :+1: : si l'utilisateur met un :+1: , on ajoute le synopsis qu'il a écrit comme synopsis correspondant à l'oeuvre pour laquelle il a mis un :+1: 
		- [ ] Voir comment utiliser l'API depuis le terminal (cf. remarques du carnet de bord du 08/02/2022)
	- [ ] Faire l'interface graphique de l'API
		- [x] Architecture basique de la page
		- [x] Première étape : peu importe le paragraphe, ça renvoie le même paragraphe
		- [x] Faire un template jinja pour faire un tableau de résultats avec le rank, le nom de l'oeuvre, et des métadata sur l'oeuvre
		    - [ ] Pour l'affichage des résultats : une fois qu'on a le titre d'une oeuvre, on peut utiliser une API pour récupérer des métadonnées. On a pas besoin de les stocker nous-mêmes dans une BDD : https://rapidapi.com/blog/movie-api/
        - [ ] Remplacer la partie "Avis" de l'interface par des exemples de résultats pour montrer les performances de notre modèle. C'est notre petit côté commercial.
- [x] Mettre en place le carnet de bord avec https://hackmd.io
- [x] Ecrire une petite liste de synopsis inventés pour l'évaluation qualitative
- [x] Augmentation des données (voir 26/02/2023) (mettre les données générées dans le même format que les données d'entraînement)
    - [x] Backtranslation => **trop long donc ça vaut pas la peine pour le peu de différences**
    - [x] summarization => **on peut pas faire tourner le script de finetuning**
- [x] Faire une V1 de l'API en faisant le lien entre l'API et le script de sentence similarity

### Aurel

- [ ] Trouver nos données d'entraînement : Aurel
	- questions
		- est-ce qu'on peut scraper nous-mêmes ? 
		- est-ce qu'on doit le faire manuellement ? 
		- est-ce qu'il existe une database déjà ?
		- format de sortie ?
	- [ ] 2 sous-tâches
		- [ ] recherche d'une BDD existante 
			- démo sur comment l'utiliser
			- écrire des fonctions rapides en python pour faire des requêtes
		- [ ] génération d'une BDD
			- démo sur comment ça scrape
			- scrapage -> création directement au format SQL
        - [x] Mettre en forme le dataset choisi (format csv)
            - [x] Dans le csv du corpus : soit mettre un nom à la colonne des identifiant, soit enlever la colonne identifiant
- [ ] Voir comment augmenter nos données
    - Truc des questions/réponses 
    - Paraphrases ?
- [x] Préparer le GitHub : Aurel
	- [ ] l'organiser avec des dossiers précis
	- [ ] écrire un guide pour savoir comment
		- [ ] le GitHub fonctionne
		- [ ] les fichiers sont nommés
- [ ] Ecrire une petite liste de synopsis inventés pour l'évaluation qualitative

### Julie

- [x] Comment fonctionne doc2vec ? : Julie
	- https://radimrehurek.com/gensim/models/doc2vec.html
- [x] Comment utiliser BERT : Julie
	- [x] sortie : faire un notebook avec une démo
	- [x] comment fine-tuner BERT
	- [x] grid search
- [x] Trouver les transformers pour les tâches
    - [x] Double fine-tuned ? Transfer learning
    - [ ] évaluation ?
    - [x] Faire un notebook pour tester
- [x] Continuer le travail sur doc2vec : **finalement, on n'a pas choisi cette option**
- [x] Notebook pour la prépratation du dataset dans le format attendu du module `transformers`
- [x] Baseline : faire une tâche de similarité 
- [ ] Autre manière : classification -> Aurelien.
    - [ ] genre
    - [ ] par film
- [x] Ecrire une petite liste de synopsis inventés pour l'évaluation qualitative
- [x] Fine tuning Sentence Transformers
    - [x] demo sur google collab fine tuning avec dataset - paire de phrases
    - [x] demo avec clustering (sans paire de phrases)
- [x] Paraphrase mining test (fonctionne bien) 
    - [x] démo pour notre baseline ? 


## :school: Tutoriel :school:

:::info
Cette section sert à écrire les tutoriels. Elle peut servir de brouillon pour la documentation qu'on devra rendre à la fin.
:::

On pourrait peut-être utiliser [Scribe](https://scribehow.com) pour faire un tutoriel, mais la version gratuite marche que dans les navigateurs.

### API

L'arborescence ressemble à ça : 

```bash
.
├── src # Scripts pour l'API
│   ├── database.db # Notre database
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
├── static # Front-end
│   ├── assets # CSS, Javascript...
│   ├── images
│   └── index.html # Notre site
└── templates # Templates JinJa
```

Pour lancer l'API : 

```bash!
cd src
uvicorn main:app --reload 
```

L'option `--reload` fait qu'on a pas besoin d'arrêter uvicorn et de le relancer à chaque fois qu'on fait une modif dans un script. On a juste à enregistrer les modifications et le rechargement se fera tout seul.

Pour accéder à notre **page HTML**, il faut aller là-dessus : http://localhost:8000/front/index.html.

Pour accéder à la **documentation** générée automatiquement par `FastAPI`, il faut aller sur ce lien : http://localhost:8000/docs#. On peut tester directement les fonctionnalités là-dedans en appuyant sur un des endpoints > "Try it out".

#### Explication rapide des scripts

- `main.py` : C'est de là qu'on lance l'API. C'est ici qu'on a écrit les points d'entrées (endpoints) pour accéder à notre API.
- `database.py` : Fait tout le setup pour la database avec SQLAlchemy. C'est ici qu'on indique où créer la database et son nom. 
- `models.py` : On définit les tables de notre BDD et les colonnes qui constituent ces tables. 
- `schemas.py` : On définit la structure des données d'entrée : on crée des classes qui étendent la classe `BaseModel` de `pydantic`. FastAPI repose sur le typage des données : c'est pour ça qu'on a besoin de typer nos données d'entrée. Chaque attribut de notre classe correspond à un item json (si j'ai bien compris). 
- `services.py` : Toutes les fonctions qui permettent de faire des opérations CRUD (Create Read Update Delete). En somme, toutes les fonctions qui permettent d'interagir avec la base de données.

#### Explication rapide du fonctionnement de l'API

Quand on lance l'API et qu'on va sur http://localhost:8000/front/index.html, ça affiche notre page HTML.

Quand on écrit quelque chose dans le formulaire et qu'on appuie sur "Trouver les oeuvres similaires", ça envoie une requête POST au endpoint `submit` de notre API. La requête se fait en Javascript, directement dans `index.html`. 

Pour l'instant, la seule chose que ce point d'entrée fait est renvoyer l'input de l'utilisateur ainsi que la longueur de cet input formaté en HTML en utilisant un template. Le template utilisé se trouve dans le dossier `templates` et il s'agit d'un template écrit en JinJa. Tout ça s'affichera juste en-dessous du formulaire.

Quand on aura mis en place tout le côté ML, on aura juste à renvoyer les vrais résultats au lieu de ça. (Je vais écrire un template JinJa pour quand on aura les résultats).


## :anchor: Carnet de bord :anchor:

:::info
Cette section sert à indiquer les progrès qu'on fait au fur et à mesure.

Mettre un titre de niveau 3 quand on change de date. Mettre un titre de niveau 4 pour indiquer qui a fait quoi.

Exemple : 
```markdown
### :calendar: 01/01/2023

#### Den

- j'ai fait ça
- et ça aussi

#### Julie

- moi j'ai fait ça

### :calendar: 02/01/2023

#### Den

- j'ai fait ça

#### Aurel

- moi ça
```
:::

### :calendar: 31/01/2022

#### Den

- J'ai pris un template HTML 5 UP pour faire le premier jet de l'interface graphique
- ✅ J'ai réussi à faire le lien entre l'interface graphique et notre API : quand on va sur http://127.0.0.1:8000/front/index.html#, qu'on écrit un synopsis et qu'on appuie sur le bouton, ça réécrit le synopsis en-dessous du formulaire avec le nombre de caractères. J'ai utilisé un template Jinja pour renvoyer le résultat. 
- 🗒️ Je vais essayer de mettre en place le lien avec une BDD fictive pour l'instant : https://fastapi.tiangolo.com/tutorial/sql-databases/ (tutoriel)
- 🗒️ Je vais aussi essayer de faire des similarités basiques pour que le bouton renvoie l'oeuvre la plus similaire parmi ma BDD fictive

### :calendar: 01/02/2023

#### Den

- ℹ️J'ai regardé un [tutoriel](https://www.youtube.com/watch?v=eltKL8kC160) pour essayer de mieux comprendre comment connecter notre API à une base de données avec SQLAlchemy
    - Le mec du tutoriel explique bien comment séparer son code en models/schemas/services : 
        - A **schema** is a blueprint that defines the structure of a database, including tables, columns, relationships, and constraints.
        - A **model** is a representation of a real-world entity, such as a user or an order, in a database. A model defines the attributes and behaviors of the entity and is used to interact with the data stored in the database.
        - **Services** are pieces of code that provide a specific functionality, such as connecting to the database, querying data, and transforming data. Services can be used by other parts of an application to access the database and perform specific tasks.
- J'ai commencé à essayer de mettre en place la BDD. 
    - 🐛 [FIXED] Pour l'instant, y'a un bug : mes tables ne se créent pas.

### :calendar: 05/02/2023

#### Den

- Continuation du travail pour la mise en place de la BDD : 
    - ✅ Ma database et ses tables se créent correctement. J'avais juste oublié une ligne dans le `main`.
    - ℹ️ [Super tutoriel](https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-1-hello-world/) qui résume un peu tout ce qu'on a vu en cours avec Jinja, FastAPI et SQLAlchemy. Il va bien avec le tutoriel vidéo que j'ai mis dans le compte-rendu du 01/02/2023
    - ✅ J'ai créé un endpoint pour peupler la base de données avec les synopsis.
    - ✅ Quand l'utilisateur submit un synopsis, en plus de renvoyer le résultat de l'API, ça enregistre le synopsis qu'il a écrit dans la table "queries" de notre base de données. A voir qu'est-ce qu'on veut que ça enregistre aussi.
        - 🐛 Par contre, même si ça marche, j'ai l'erreur suivante : "SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 16768 and this is thread id 12796."
    - ❔ J'avais une erreur à un moment à cause des autorisations CORS (?), mais Aurélien l'a réglé en mentionnant ça dans `main.py` : 
        ```python
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["POST"],
        )
        ```
        C'est un peu chelou parce que j'avais eu la même erreur à un moment mais j'avais réussi à la régler et elle est revenue.
- Ecriture d'un petit tutoriel sur comment marche l'API.
- Objectif pour la suite : 
    - [x] Ecrire un meilleur template pour que ça renvoie les résultats des oeuvres similaires sous la forme d'un tableau avec le rang, le résumé de l'oeuvre, et les métadonnées
    - [x] Faire en sorte de pouvoir mettre un :-1: ou :+1: sur chaque résultat.

#### Julie

- J'ai fait les notebooks pour l'utilisation de \:
    - BERT 
    - fine-tuned BERT
    - doc2vec

### :calendar: 08/02/2023

#### Réunion

- Mise à jour du cahier des charges après la mise en commun
- Mise en place du GitHub
    - Choix du nom du répertoire Git : JADe Project (Julie Aurélien Den ensemble)
    - Créer l'arborescence des dossiers.
- Remarques sur la mise en commun
    - API
        - Comment faire pour que l'API soit à la fois utilisable via des requêtes CURL **et** via notre interface graphique : 
            - Comme on utilise un template Jinja, notre endpoint "submit" renvoie du HTML. Mais quand on passe par le terminal, on s'attend plutôt à recevoir du JSON, non ? 
            - Est-ce que je devrais faire deux endpoints différents : un pour l'interface graphique qui renvoie du HTML et un pour passer par le terminal et qui renvoie du json ?
    - Corpus
        - Pour l'instant, on s'en tient aux films et aux séries. On verra après pour les livres. 
        - Pour le corpus, on choisit [ce corpus](https://www.kaggle.com/datasets/linggarmaretva/movie-synopsis-dataset) avec 8 000 films.

#### Den

- ✅ J'ai réussi à régler le bug "SQLite objects created in a thread can only be used in that same thread" : il fallait rajouter la ligne `connect_args={'check_same_thread':False}` dans les arguments de `create_engine()`.
- J'ai créé une *toute petite* base de données (10 films) pour faire des tests pour l'affichage des réusltats sous la forme d'un tableau : 
    - Pour tester : on rentre 1 mot dans le formulaire et ça affiche un tableau des titres des films (et leur date de publication) dont le synopsis contient ce mot.

### :calendar: 12/02/2023

#### Den

- Objectifs pour aujourd'hui : 
    - [x] rendre la table des résultats plus jolie
    - [x] ajouter le synopsis dans la table des résultats
    - [x] mettre le lien vers le github
    - [x] changer le background
- ✅ J'avais un problème à un moment avec le CSS : à chaque fois que je le modifiais, ça changeait rien à l'apparence du site. C'est parce que ça utilisait le CSS qu'il avait cached. Pour régler ça, on peut append une query random (on ajoute `?id=1234` à la fin du chemin vers la feuille de style). Ca l'oblige à reload si j'ai bien compris.
    ```html
    <link rel="stylesheet" href="assets/css/main.css?id=1234" />
    ```
- :sparkle: J'ai changé le background.
- J'ai mis le lien vers notre GitHub : quand on appuie sur l'icône, ça renvoie à notre répertoire.
- :sparkle: Modification de l'apparence de la table des résultats
    - J'ai modifié le template `result_table.html.jinja` pour indiquer que la table faisait partie de la classe `default`. Elle est plus jolie maintenant. 
    - J'ai ajouté le synopsis dans la table des résultats.
    - :new: J'ai mis un bouton thumb-up pour que l'utilisateur puisse donner son avis mais pour l'instant il fait rien parce que j'ai pas réussi à le faire fonctionner.

### :calendar: 15/02/2023

#### Julie

- ✅J'ai trouvé le moyen d'utiliser nos propres données pour les transformers (ils sont au bon format). Pour le moment ça fonctionne ainsi : 
    - Un .csv pour le train
    - Un .csv pour le test
- :warning: Il y a un problème si je prends le .csv et que je split, je ne sais pas encore trop pourquoi... 
- ✅Le reste du script fonctionne (cf google colab `demo_transformers_and_doc2vec.ipynb`) :warning:  mais le transformers choisi n'est pas bon. Je n'ai pas encore cherché lequel il faudrait prendre pour notre tâche.
- ✅ J'ai ajouté le `Grid Search` sur le google collab

### :calendar: 16/02/2023

#### Réunion 

- On peut pas vraiment faire d'évaluation quantitative, mais on peut faire une petite évaluation qualitative : chacun crée une petite liste de synopsis inventés et on juge à l'oeil
- Similarité basique serait notre baseline
- Transfer-learning pour voir si on peut dépasser notre baseline : Faire une première classification en genre ou un autre type de clusterisation sinon le classifieur va faire de l'overfitting et après l'entraîner à trouver les oeuvres

### :calendar: 19/02/2023

#### Den

-  ✅ :sparkle: [BRANCHE `styleAPI`] J'ai bougé le commit pour l'ajout du nouveau background dans la bonne branche (`featureReview` > `styleAPI`)
- :new: [BRANCHE `returnJSON`] J'ai réussi à faire en sorte que suivant depuis où on fait une requête, ça ne renvoie pas le même format : 
    - Si on fait un CURL depuis le terminal, ça renvoie les résultats sous la forme d'une liste de dictionnaires
        - :question: Je comprends pas trop encore si ça c'est l'équivalent du JSON ? J'ai du mal à comprendre c'est quoi le JSON exactement.
        - :bug: Ca marche quand je vais sur http://127.0.0.1:8000/docs#, mais pas quand je teste depuis mon terminal : `Failed to connect to 127.0.0.1 port 8000: Connection refused`
    - Si on fait une requête depuis l'interface graphique, ça renvoie les résultats sous la forme d'un tableau HTML en utilisant un template JINJA. 
- [BRANCHE `featureReview`] J'ai continué à essayer de mettre en place la prise en compte des avis utilisateurs avec les :-1: et :+1:. 
    -  Pour l'instant, quand on clique sur un bouton thumb-down/up, les actions suivantes s'effectuent :
        - Print dans la console pour indiquer quel bouton a été cliqué
        - Quand le thumb-up-button est cliqué, il devient vert
        - Quand le thumb-down-button est cliqué, il devient rouge
        - Si un bouton avait déjà été cliqué et que l'utilisateur appuie sur un autre, le bouton cliqué en premier redevient gris et le bouton cliqué en deuxième devient rouge/vert (selon si c'est un up ou un down)
    - :bug: [FIXED] Problème : comme l'ID des boutons est attribué dans le template JINJA et que c'est le même ID pour toutes les lignes du tableau, les couleurs changent seulement pour les pouces de la première ligne du tableau (car les IDs ont été attribués en premier à cette ligne). Quand on clique sur les pouces des lignes en dessous, les actions listées au-dessus fonctionnent mais le changement de couleur n'est reflété que pour la première ligne du tableau. Par exemple, si pour la ligne #1, j'ai cliqué le thumb-up-button, il va devenir vert. Si je clique ensuite pour la ligne #9 sur le thumb-down-button, le thumb-down-button de cette ligne va rester gris mais celui de la ligne #1 va devenir rouge (et le thumb-up-button de la ligne #1 va redevenir gris).
- :writing_hand: Ecriture de quelques synopsis à tester pour l'évaluation qualitative de plus tard.

Synopsis à tester : 

- I'm looking for a coming-of-age movie in which the daughter is very close to her mother but one day, they have a big fight and stop talking to each other. The movie is about them forgiving each other.
- I want to watch a movie set in the far future. It's a post-apocalyptic movie but there are no zombies, only robots. 
- movie roaring twenties documentary
- i want a movie with animals and they talk and everyone is friends. 

### :calendar: 20/02/2023

#### Den

- ✅ :sparkle: [BRANCHE `styleAPI`] Renommage de la section "avis" en "demo" : On avait une section "Avis" dans laquelle je comptais mettre un moyen de donner son avis sur l'API. Au final, on va passer par un système de thumb-up/thumb-down directement lorsqu'on affiche les résultats de la requête. Du coup j'ai changé la section "avis" en une section "demo" dans laquelle on mettra des exemples de requêtes avec les résultats obtenus pour showcase notre API.
- ✅ :recycle: [BRANCHE `moveJS`] J'ai bougé le javascript qui se trouvait dans `index.html` pour l'appel à notre API dans un fichier `.js` à part pour que ça soit plus clair.
- [BRANCHE `featureReview`] 
    - ✅ J'ai réussi à régler le problème avec les couleurs des boutons thumb-up/thumb-down (voir 19/02/2023)
        - :warning: [DONE] Il reste encore à améliorer le code `thumbUp.js`. Dedans il y a deux fonctions différentes (une quand on clique un thumb-up et une quand on clique un thumb-down), mais au final elles sont très similaires.
    - :new: Quand l'utilisateur met un thumb-up à une des oeuvres, une nouvelle entrée est écrite dans la base de données pour cette oeuvre avec comme synopsis le synopsis écrit par l'utilisateur. 
        - Pour ça, j'ai modifié un peu la fonction `submit()` dans `main.py` pour que ça renvoie aussi la requête de l'utilisateur. Comme le script est appelé depuis le template JINJA, je pouvais pas juste la récupérer depuis `index.html`. 
        - :warning: [DONE] Pour l'instant, j'ai pas encore réglé le problème de si l'utilisateur change d'avis et enlève son thumb-up pour mettre un thumb-down. Je pense qu'il faut que je crée une fonction qui delete une entrée de la BDD. 

### :calendar: 22/02/2022

#### Den

- :question: Mais du coup imaginons que quelqu'un écrit un synopsis nul, mais il met des thumb-up à des résultats. Est-ce que ça veut dire qu'à un autre utilisateur, on pourrait renvoyer ce même synopsis nul ?
    - Ou alors il faudrait passer par l'API externe. On se sert des données des utilisateurs que pour entraîner et sinon on passe par l'API externe pour récupérer les synopsis qui sont renvoyés à un utilisateur. 
- J'ai changé le nom du POST endpoint `synopsis` en `similar-works`, parce que c'est plus clair. 
- :question: J'ai essayé de changer le endpoint POST `similar-works` en endpoint GET parce que je me suis dit que ça faisait plus sens. Mais j'arrive pas à le faire fonctionner. Après, je sais pas si c'est très utile de changer. De toute façon, ça fait ce qu'on veut que ça fasse. C'est juste que c'est pas très logique du POV de comment ça fonctionne. 
- ✅ [BRANCHE `featureReview`] Continuation de la prise en charge de l'avis utilisateur
    - ✅ Prise en charge du changement d'avis de l'utilisateur : si jamais l'utilisateur met un thumb-up, ça rajoute le synopsis dans la BDD. S'il change d'avis et met un thumb-down, il faut mettre en place quelque chose pour supprimer le synopsis de la BDD : 
        - ✅ J'ai écrit la fonction pour supprimer le synopsis de la BDD. 
          - NOTE : si plusieurs synopsis identiques pour la même oeuvre exactement exsitent, ça ne supprime qu'un seul.
        - ✅ J'ai réussi à faire le lien entre le thumb-down button et la BDD : quand un utilisateur appuie sur le thumb-down-button, ça supprime bien la ligne de la BDD avec la requête qu'il a écrite. 
            - Si la requête n'est pas trouvée (ex : l'utilisateur a appuyé plusieurs fois sur le bouton donc elle a déjà été supprimée) une erreur 404 est levée.
            - J'ai dû modifier un peu `main.py` pour autoriser l'accès aux requêtes DELETE, comme on avait fait pour les requêtes POST (voir 05/02/2023)
    - ✅ J'ai amélioré le script `thumbUp.js` pour qu'il y ait moins de répétitions dans le code. Sinon les deux fonctions (celle pour thumb-up et celle pour thumb-down) se ressemblaient vraiment trop 

### :calendar: 23/02/2023

#### Den

- Pour augmenter notre corpus ou pour créer des paires de synopsis similaires, on pourrait faire : 
    1. **backtranslation** : on traduit dans une langue target et on retraduit dans la langue source
        - Je pense qu'il faudra lire des trucs sur ça parce que c'est possible que toutes les paires de langue ne marchent pas aussi bien ensemble. 
    3. **summarization** : partir de la partie "plot" détaillée de Wikipédia pour faire un résumé. En plus on pourrait l'évaluer en comparant le résultat obtenu au "summary" de wikipédia ou à un synopsis tiré d'un autre site. 
    
    :::info
    On a parlé avec Pierre et ouais il a dit que ça serait bien de commencer avec de la backtranslation, et après de passer à summarization. 
    
    Je crois qu'il a parlé de voir le problème dans l'autre sens : genre la requête de l'utilisateur est un résumé du synopsis ou je sais pas quoi. Faut demander à Aurélien.
    
    On peut aussi juste faire appel à des APIs extérieur.
    :::
 
#### Julie 

- publication sur github de `Sentence_Similarity.ipynb. Ce notebook est une première version de notre système. On utilise les Sentences Transformers pour transformer les synopsis en embedding, et ensuite on calcule la distance cosinus pour trouver les paires les plus proches d'un synopsis / d'une requête donnée. 
- Maintenant, il faut trouver comment fine-tuner ce transformers. 

### :calendar: 26/02/2023

#### Réunion

- il faudra d'abord tester avec et sans augmentation pour voir si améliore le modèle
- augmentation des données
    - backtranslation : essayer avec d'autres langues que le français
    - translation : prendre les pages écrites dans d'autres langues 
    - summarization : prendre des résumés détaillés et créer des synopsis plus courts
- pour fine-tuner notre modèle
    - tuto déjà trouvé, on a juste à mettre nos données en forme
    - composer des phrases non-similaires en prenant la traduction d'une oeuvre et le synopsis d'une autre oeuvre
    - clusterisation ?
- discussion avec Pierre
    - sonder un réseau de neurones
        - entraîner un transformer à générer des résumés à partir des oeuvres intégrales
        - après, une fois qu'il est entraîné, on peut faire le chemin inverse : on traite le résumé comme une sortie du réseau de neurones et on demande au transformer du coup c'était quoi l'input ? 
- recherche de paraphrases
    - au lieu de faire une distance cosinus, on pourrait passer par un truc qui compare des paires de phrases et attribue un score de 0 à 1 selon si c'est des paraphrases ou pas
- Envoi d'un mail à Grobol pour prendre un rendez-vous

:::warning
:exclamation: :exclamation: D'ici le RDV avec Grobol : 

- Julie : continuer de chercher sur comment fine-tuner -> discussions
- Aurélien : 
    - chercher comment faire la classification, notamment avec un truc plus basique qu'un transformer
    - recherche sur "sonder réseau de neurones"
- Den : 
    - faire le lien entre le truc basique sentence_similarity
    - mettre en place les machins pour augmenter les données
        - mettre les données générées dans le même format que les données d'entraînement
:::

### :calendar: 27/02/2023

#### Den

- ✅ :sparkle: Je suis repassée sur le script `sentence_similarity.py` pour le commneter et le nettoyer un peu. Il est dans `app/src/scripts`.
- :new: ✅ J'ai réussi à mettre en place un système de versionage de l'API. 
    - :new: La `v0` correspond au truc basique que j'avais fait pour m'assurer que le lien entre l'API et le front fonctionnait : quand un utilisateur écrit un mot, ça renvoie les oeuvres dont le synopsis contient ce mot. 
        - Quand on fera de nouvelles versions, on aura toujours accès aux anciennes version de l'API via le terminal. 
        - :warning: Par contre, l'interface graphique correspondra toujours à la version la plus récente parce que je code en dur la version de l'API à utiliser. On peut toujours accéder à la version avec tous les fichiers fonctionnels en allant dans les tags de notre GitHub : https://github.com/AurelienSH/JADe_project1/releases/tag/v0
    - :new: [BRANCHE `versionAPI`] Dans la `v1`, j'ai implémenté le truc de `sentence_similarity`
        - :warning: C'est un peu cra-cra. Ca renvoie une liste de dictionnaires. Encore une fois, aucune idée de si c'est équivalent à du JSON (voir 19/02/2023)
        - Maintenant pour accéder à la docs de la version 1, il faut aller sur : http://localhost:8000/api/v1/docs.

### :calendar: 28/02/2023

#### Julie

- Ecriture d'un notebook avec d'autres manières de calculer la similarité entre nos documents `Autre_Sentence_Similarity.ipynb`
	- KNN
	- distance euclidienne
- Recherche comment Fine-Tuner le modèle

### :calendar: 01/03/2023

#### Den

- :question: On pourrait peut-être fine-tuner un modèle de summarization : on le fine-tune sur un corpus de detailed plots et la target c'est le synopsis court.
    - masquer des endroits pour que ça génère pas le meme summary et que ça se focalise pas sur les mêmes plot points ?
    - Score "ROUGE" pour l'évaluation de notre modèle fine-tuné pour la summarization : Recall-Oriented Understudy for Gisting Evaluation
- :new: A partir d'un corpus de plots wikipédia [`wikiPlots`](https://github.com/markriedl/WikiPlots) et du corpus de [synopsis IMDB](https://www.kaggle.com/datasets/linggarmaretva/movie-synopsis-dataset), j'ai fait un corpus de 9807 oeuvres. Pour chaque oeuvre, on a un tuple qui contient : le titre de l'oeuvre, le plot détaillé provenant de Wikipédia, le synopsis court de IMDB.
- Pour ajouter des fichiers de plus de 100MB sur le git : 
    ```bash
    sudo apt-get install git-lfs
    git lfs install
    git lfs track gros_fichier
    ```
    Après on a plus qu'à faire `git add` avec les fichiers qu'on veut (pas besoin de `add` les gros fichiers) et de push.

### :calendar: 02/03/2023

#### Réunion 

- Aurélien : normalement script fonctionnel pour entraîner classifieur
- Den : 
    - [ ] backtranslation : 
        - [ ] regarder si les résultats sont mieux avec l'allemand
        - [ ] créer le corpus augmenté 
    - [ ] summarization : 
        - [ ] faire tourner le truc de fine-tuning
        - [ ] si le fine-tuning a fonctionné, créer le corpus augmenté
    - [ ] ajouter un lien vers le site contenant la documentation dans notre API


:::warning
on voulait intégrer un truc pour calculer le coût écologique, il faut pas qu'on oublie :
https://codecarbon.io
https://mlco2.github.io/impact/
https://huggingface.co/blog/carbon-emissions-on-the-hub
:::

#### Den

- ✅ Correction d'une erreur dans le corpus `imdb_wiki_corpus`:
    - J'avais fait une erreur dans la constitution du corpus imdb_wiki_corpus. J'avais oublié de vider ma liste tampon donc c'est pour ça que le fichier était énorme. J'ai corrigé l'erreur.
    - J'ai aussi vu dans un tuto qu'il fallait le mettre dans un autre format. Du coup au lieu de passer par une liste de tuples dans laquelle chaque tuple contient (title, synopsis IMDB, plot wiki), j'ai fait un CSV avec seulement deux colonnes :
        - "document" : le plot détaillé Wikipédia
        - "summary" : le synopsis IMDB court
- :new: J'ai fait un notebook (`test/FR_summarizer.ipynb`) pour fine-tuner sur `imdb_wiki_corpus` le modèle mT5 pour la tâche de summarization. J'ai suivi ce [tuto](https://huggingface.co/course/chapter7/5?fw=pt). Je l'ai pas encore lancé parce que ça va prendre longtemps mais ça a l'air de marcher parce que quand j'ai commencé à le lancer, ça m'a bien créé le truc sur huggingface et sur mon pc.
- :warning: J'ai voulu créé le dataset augmenté par backtranslation sauf que j'ai fait un test sur 3 oeuvres et vraiment, les synopsis générés sont quasi-identifiques à un mot près à chaque fois.

### :calendar: 06/03/2023

#### Julie

- Fine tuning de notre Sentence Transformers de deux manières :
1. utilisation de la triplet loss : j'ai augmenté les données manuellement en créant des requêtes associées aux synopsis (50). J'ai ensuite utilisé le triplet synopsis, requete associée, requete non associé, pour fine-tuner le transformers.
2. crowdsourcing : il est possible d'utiliser les avis des utilsiateurs pour fine-tuner notre modèle (niveau de statisfaction). -> écriture du code qui sera implémenter plus tard.

### :calendar: 07/03/2023

#### Réunion

- Manière dont on a fine-tuné : 
    - `query positive` = la requête écrite par un utilisateur et qui représente un bon synopsis pour une oeuvre donnée
    - `query negative` = la requête écrite par un utilisateur et qui repésente un mauvais synopsis pour une oeuvre donnée
    - Pour une oeuvre donnée, le but est de réduire la distance cosinus des embeddings entre le synopsis de l'oeuvre et la `query positive` et d'augmenter la distance avec la `query negative`. Le modèle fine-tuné permet d'obtenir des meilleurs embeddings pour notre tâche.
    - Du coup on peut utiliser les thumbs-down et thumb-up des utilisateurs : 
        - Si l'utilisateur met un thumb-down, arbitrairement on attribue la distance cosinus de 1.5 (très peu similaire).
        - Si l'utilisateur met un thumb-up, arbitrairement on attribue la distance cosinus de 0.2 (très similaire)
- [x] Faire le planning pour la journée du 08/03/2023
- Idées pour la suite : permettre à l'utilisateur de rajouter une oeuvre dans la BDD

---

Objectifs pour le 08/03/2023:

- [ ] DEN : Passer le notebook `Autre_Sentence_Similarity` en script (repartir du script `app/src/scripts/sentence_similarity.py`)
    - [ ] Nettoyer le script
    - [ ] Commenter le script
- [ ] AUREL : Faire l'évaluation qualitative de notre modèle avec et sans fine-tuning
    - [ ] Ecrire plusieurs queries
    - [ ] Faire un tableau des oeuvres les plus similaires selon notre modèle avec et sans fine-tuning
    - [ ] Refléchir à comment mesurer la qualité du modèle
- [ ] DEN : Implémenter le modèle fine-tuné dans notre API
    - [x] Changer la manière dont on store les thumb-up/thumb-down dans notre BDD SQL
        - [x] Updater les schémas
        - [x] Updater les modèles
        - [x] Peut-être un `back-populates` avec une liste ? Un truc comme ça : **Finalement on a pas choisi ça mais c'est fonctionnel ce qu'on a fait**
            |  SYNOPSIS  | QUERY POS | QUERY NEG |
            | :---------:| :--------- | :--------- |
            | a girl drinks and reveals she's in love with her best friend | ["story about two best friends falling in love", "a boy and a girl fall in love and they happen to be best friends"] | ["story about aliens", "two brothers fighting"]|
    - [x] Faire le lien entre le script pour fine-tuner et notre BDD SQL : 
        - [x] Faire en sorte que le script pour fine-tuner utilise bien en entrée les données qui se trouve dans notre BDD pour créer les Triplets.
    - [ ] Publier une V2 de l'API qui utilise le modèle fine-tuné 
        - Je pense qu'en soit il y aura surtout à changer le chemin du modèle utilisé
    - [x] Regarder si on peut trouver un moyen de faire un script pour que ça fine-tune automatiquement tous les X temps
        - Peut-être un dossier `last_fine_tuned_model` dans lequel il y a le dernier modèle à utiliser par notre API, et à chaque fois qu'on re-fine-tune, ça déplace l'avant-dernier modèle dans un dossier `history_models`. 
        - Selon Aurélien, il y a moyen d'automatiser : le script se lance toutes les semaines par exemple.
- [x] AUREL : Essayer de lancer le truc de classification : **Ne fonctionne pas**
- [x] Essayer d'augmenter les données
    - [x] Backtranslation : **TROP LONG**
        - [x] Voir si ça marche mieux avec l'allemand
        - [x] Ecrire le script pour l'écriture du corpus (même format que le corpus de base)
        - [x] Créer le corpus augmenté par backtranslation
    - [x] Summarization : **Ne fonctionne pas**
        - [x] Fine-tuner summarizer
        - [x] créer le corpus augmenté par summarization
- [ ] Petites bricoles si on a le temps : 
    - [x] Changer le nom de notre site en "SynSearch"
    - [ ] Utiliser une API externe pour récupérer les images des films et la date de publication du film
    - [x] Améliorer la manière dont j'ai implémenté l'utilisation du modèle dans notre API
        - Pour l'instant je fais ça de manière hyper cracra : je charge les modèles dans le script `app/src/services.py`, mais peut-être qu'il y a une manière plus efficace et plus rapide. 
        - [x] Changer `pickle` pour le chargement des modèles

### :calendar: 08/03/2023

#### Den

- Mise en place de la V2 qui utilise le modèle fine-tuné : 
    - Modification des schémas et models pour la BDD
    - Modification du template JINJA `result_table` et du script `sentence_similarity` pour que ne garder que les colonnes relevant (celles qui ont été gardées après remodélisation de la BDD)
    - Modification de `thumbUp.js` pour faire le lien entre la nouvelle BDD SQL et l'API : quand on met un thumb-up, ça rajoute une ligne dans la table `Review`. Par exemple :
        | id | title | synopsis | query | score |
        | ---| ----- | -------- | ----- | ----- |
        | 0  | the notebook | love love love | a love story | pos|
- Changement du titre de notre site en "SynSearch"

#### Julie

-  Rédaction de la documentation 
    - Mise en place des différentes pages avec les liens
    - Initialisation de docsify 
    - Publication du site avec GitHub Page
- écriture de synopsis pour l'évaluation du système
- trier les scripts utilisés pour l'utilisation des transformers / pour les différents tests des pistes envisagées pour les ajouter plus tard au github.

### :calendar: 12/03/2023

#### Den & Aurel

- ✅ Implémentation du finetuning directement dans l'API : 
    - Grâce au script `app/src/scripts/utils.py`, à chaque fois que l'API est lancée, ça vérifie automatiquement si un finetuning doit être fait. On considère qu'un finetuning est nécessaire si une semaine s'est écoulée depuis le dernier finetuning.
    - Le finetuning se fait bien sur les données qui sont conservées dans la BDD
    - On conserve les 5 derniers modèles finetunés dans le dossier d'archives dans le dossier `models`
    - Après chaque finetuning, les embeddings du corpus sont recalculés avec le modèle finetuné et le fichier pickled `app/embeddings/embeddings_FT_corpus_movie` est updaté
- Nettoyage global du git 
    - Renommage du script `app/src/scripts/sentence_similarity.py` en `similarity.py` parce que ça faisait plus sens. 
    - On a bougé les fonctions de lecture de corpus et de création des embeddings dans un script `preprocesing.py` pour éviter la redondance. 
    - Nettoyage du notebook `Autre_Sentence_Similarity` : j'ai bougé tout ce qui avait à voir avec le premier finetuning (= sur le corpus augmenté manuellement) dans un script à part (`app/src/scripts/finetune_first_model.py`). Ce script ne sera jamais lancée une deuxième fois mais on l'a laissé dans le git pour montrer comment le premier finetuning a été fait. Les autres finetuning seront fait avec les données collectées dans la BDD SQL. 
    - Suppression de certains scripts qui ne servaient plus à rien
- Avant j'avais enregistré le modèle non-finetuné sous la forme d'un fichier pickled. J'ai changé ça pour que ça sauvegarde bien le modèle dans un dossier et qu'on le charge comme c'est censé être chargé. 

### :calendar: 19/03/2023

#### Den

- Nettoyage global des scripts
- Ecriture des queries pour l'évaluation qualitative
- Ajout du lien vers la documentation sur l'interface graphique de l'API
- Modification du footer de `index.html` pour mettre nos noms

### :calendar: 14/03/2023

#### Den

- Continuation du nettoyage du git 
    - Passage du HTML dans le validateur de W3School
    - Suppression d'un template JINJA obsolète car seulement utilisé dans la V0 de l'API (j'ai supprimé tout ce qui est relatif à la V0 parce que de toute manière, avec tous les changemens qu'on a fait, elle ne marche plus. Une version "fonctionelle" se trouve dans les tags
    - Suppression des branches obsolètes
- Ajout d'un notebook de demo (`demo/synsearch_requests.ipynb`) qui permet de tester des requêtes à l'API en passant par le module python `requests`.

### :calendar: 15/03/2023

#### Den

- Continuation du nettoyage du git
    - Nettoyage du dossier `test`
    - Déplacement du notebook `test/make_dataset_imdb_wiki.ipynb` dans le dossier `Data/scripts` car plus approprié
    - Merge de toutes les branches dans le main

Tâches à finir : 

- [x] Lier le hackMD au git
- [ ] sélectionner quelques bons trucs pour mettre dans l'onglet "demo" de l'interface graphique
- [ ] nettoyer le requirements.txt
- [x] on a fait une baseline avec glove/word2vec????? **NON**
- [ ] Commenter et faire la docstring des scripts : 
    - [ ] `utils.py`
    - [ ] `finetuning.py`
- [ ] Publier la V2 finalisée et bien tester toutes les versions pour être sûre que tout marche
    - [ ] Créer le tag pour la V2
- [ ] regarder comment faire une requête POST depuis le terminal parce que pour l'instant ça me dit que l'accès n'est pas autorisé
- [ ] Rédiger ma partie sur la documentation
