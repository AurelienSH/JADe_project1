# Data

## Source

Les données proviennent du Movie Synopsis Dataset de LINGGAR MARETVA CENDANI. Elles sont disponibles sur [Kaggle](https://www.kaggle.com/datasets/linggarmaretva/movie-synopsis-dataset). Le corpus est au format `.csv` et contient 8484 synopsis. Le fichier se trouve dans `Data/movie_synopsis.csv`. 

Voici un exemple de ligne : 

| id | synopsis | title      |
|----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| 0  | It's Ted the Bellhop's first night on the job...and the hotel's very unusual guests are about to place him in some outrageous predicaments. It seems that this evening's room service is serving up one unbelievable happening after another. | Four Rooms |

## Augmentation des données 

### Augmentation manuelle

Pour le fine-tuning, nous avions besoin de données supplémentaires. Nous avons associé des requêtes au synopsis pour pouvoir faire notre [fine-tuning](02_systeme.md#fine-tuning). Etant donné que cela est long à faire, nous avons créée uniquement 50 requêtes. 

Voici deux exemples : 

| id | synopsis | title          | **query**                                                          |
|----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|-----------------------------------------------------------------|
| 0  | It's Ted the Bellhop's first night on the job...and the hotel's very unusual guests are about to place him in some outrageous predicaments. It seems that this evening's room service is serving up one unbelievable happening after another.                                                                                                                                                                    | Four Rooms     | **I want to watch a quirky and chaotic comedy movie**              |
| 1  | While racing to a boxing match, Frank, Mike, John and Rey get more than they bargained for. A wrong turn lands them directly in the path of Fallon, a vicious, wise-cracking drug lord. After accidentally witnessing Fallon murder a disloyal henchman, the four become his unwilling prey in a savage game of cat & mouse as they are mercilessly stalked through the urban jungle in this taut suspense drama | Judgment Night | **I'm in the mood for an intense and action-packed thriller movie** |

Le corpus augmenté manuellement se trouve dans le dossier `Data/movie_synopsis_augmented.csv`.

### Augmentation automatique

L'augmentation automatique des données n'a pas encore été réussie. Cela est dû à un problème de performance de nos machines : elles n'étaient pas assez puissantes pour lancer nos scripts, en tout cas avec un temps raisonnable de calcul. Néanmoins, les traces de notre travail se trouvent dans la section [mettre la bonne section ici](05_methodologie.md#pour-les-données-et-leur-augmentation)

