# Data

## Source


Au final, nous avons un fichier .csv qui contient 8484 synopsis. Ce fichier se trouve dans le dossier `Data`/`movie_synopsis.csv`. 

Voici un exemple de ligne : 

| id | synopsis | title      |
|----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| 0  | It's Ted the Bellhop's first night on the job...and the hotel's very unusual guests are about to place him in some outrageous predicaments. It seems that this evening's room service is serving up one unbelievable happening after another. | Four Rooms |

## Augmentation des données 

### Augmentation manuelle : *queries*

Pour le fine-tuning, nous avions besoin de données supplémentaires. Nous avons associé des requêtes au synopsis pour pouvoir faire notre  [fine-tuning](systeme.md). Etant donné que cela est long à faire, nous avons créée uniquement 50 requêtes. 

Voici un exemple : 

| id | synopsis | title          | **query**                                                          |
|----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|-----------------------------------------------------------------|
| 0  | It's Ted the Bellhop's first night on the job...and the hotel's very unusual guests are about to place him in some outrageous predicaments. It seems that this evening's room service is serving up one unbelievable happening after another.                                                                                                                                                                    | Four Rooms     | **I want to watch a quirky and chaotic comedy movie**              |
| 1  | While racing to a boxing match, Frank, Mike, John and Rey get more than they bargained for. A wrong turn lands them directly in the path of Fallon, a vicious, wise-cracking drug lord. After accidentally witnessing Fallon murder a disloyal henchman, the four become his unwilling prey in a savage game of cat & mouse as they are mercilessly stalked through the urban jungle in this taut suspense drama | Judgment Night | **I'm in the mood for an intense and action-packed thriller movie** |

Ce fichier se trouve dans le dossier `Data`/`movie_synopsis_augmented.csv`. 


### Augmentation automatique (si réussi, sinon à mettre dans la partie méthodologie)

Nous n'avons pas réussi à augmenter automatiquement nos données. Cela est dû à un problème sur nos machines : nous n'avions pas assez de capacité pour lancer nos scripts. Les traces de notre travail sont [ici](methodologie.md#pour-les-données-et-leur-augmentation))

