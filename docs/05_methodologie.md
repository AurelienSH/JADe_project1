# Méthodologie 

## Répartition du travail 

La répartition du travail s'est fait de la manière suivante : 
- Aurélien était chargé des données, de la gestion du github et de l'évaluation du système 
- Delphine a pris en main l'interface web et la gestion de l'équipe.
- Julie s'est occupée de la partie système et de la rédaction de la documentation. 

Au delà du partage des tâches, nous nous sommes toujours aidés quand il y avait des difficultés dans nos parties. 

## Suivis du travail 

Delphine a mis en place un document [*hack.md*](https://hackmd.io/13aKsikiTVmVB0Kd4qSuYw?both) pour assurer le suivis du projet et la répartition des tâches. 

## Travail intermédiaire

-> citer les documents à retrouver dans le github comme trace du travail. 

Le travail effectué pour le fonctionnement du système se trouve dans le notebook `system_test`/`Sentence_Similarity_test.ipynb`. Ce notebook contient les différentes fonctions utilisées pour faire fonctionner le système. Ce notebook contient également plusieurs tests sur le calcul de similarité (avec la distance euclidienne et les KNN). Nous avons gardé uniquement la distance cosinus dans notre projet. 

## Les autres pistes envisagées 

### Pour les données et leur augmentation

#### Back Translation

#### Summarization

### Pour le système

#### Classification avec BERT

#### Doc2Vec

Nous avons considéré, au début, d'utiliser Doc2Vec pour obtenir les embeddings de nos documents. Néanmoins, nous avons préféré l'option des Sentences Transformers car nous pouvions les personnaliser avec le fine-tuning. Un tutoriel sur le fonctionnement de Doc2Vec est disponible dans le dossier `system_test` : `demo_transformers_and_doc2vec.ipynb`

####

## Et après ? 

On pourrait envisager d'enrichir encore la base de donnée de nouveaux synopsis, et de faire fonctionner l'augmentation automatique de données. 

De plus, pour le moment, notre corpus est exclusivement en anglais. Il pourrait être envisageable d'en faire un système multilingue. 
