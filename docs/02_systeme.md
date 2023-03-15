# Système : Behind the Scenes of the API

Cette section décrit le système utilisé pour faire foncitonner :clapper: *SynSearch*.

Toutes les données utilisées proviennent de [Hugging Face](https://huggingface.co/) :hugs: et de [SBERT](https://www.sbert.net/index.html).

## Modèle choisi 

Nous avons choisi d'utiliser des Sentences Transformers pour avoir une représentation en vecteur de nos données. Plus précisément, nous avons choisi le modèle [`all-MiniLM-L12-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2). Dans le cadre de :clapper: *SynSearch* et des délais impartis, les écarts de performance entre les différents modèles est totalement négligeable. Nous avons donc simplement choisi le premier que nous avons trouvé et qui était beaucoup utilisé. 

Nous avons choisi d'utiliser des Sentences Transformers car ces transformers sont une référence dans l'état de l'art pour les embeddings de documents. De plus, ils sont faciles à utiliser et rapide à fine-tuner. Pour voir les autres options que l'on a envisagé, c'est par [là](05_methodologie.md#pour-le-système). 

Une fois le modèle choisi, nous l'avons utilisé pour encoder nos documents textuelles (les synopsis) pour en avoir une représentation numérique (sous forme de vecteur). Nous avons utilisé le même modèle pour encoder la requête de l'utilisateur.

Cela permet de calculer la distance cosinus entre la requête d'un utilisateur et le synopsis d'un film. Plus la distance est faible, plus la requête et le synopsis sont proches. Ainsi, on suggère les cinq films les plus proches de la requête à l'utilisateur. 

>[!note]
>Notre API implémente la distance cosinus mais il serait également possible d'utiliser la distance euclidienne, ou tout autre distance.

## Finetuning 
 
Plusieurs pistes pour le finetuning étaient possibles. Toutefois, elles demandaient toutes un autre format de données que celui que nous avions. Nous avons retenu deux fonctions de pertes pour fine-tuner notre modèle :

- La Triplet Loss
- La Cosinus Similarity Loss

### Triplet Loss

Les requêtes des utilisateurs ne sont pas vraiment semblables au synopsis de films. C'est pour cela qu'il fallait qu'un finetuning de notre modèle, pour ainsi prendre en comtpe le format des requêtes des utilisateur. 

Les données utilisées pour la (Triplet Loss)[https://www.sbert.net/docs/package_reference/losses.html#tripletloss] doivent comporter trois arguments : 

- Anchor : le synopsis du film dans notre BDD
- Positive example : une requête correspondant au synopsis
- Negative example : une requête ne correspondant pas au synopsis

Ainsi, on peut finetuner notre modèle pour que le format des requêtes des utilisateurs soit pris en compte par le modèle lors du calcul de similarité. Pour avoir ce format de dataset, nous avons [augmenté manuellement nos données](01_data.md#augmentation-manuelle).

Cette méthode a permis d'améliorer les suggestions en rapprochant les requêtes et les synopsis déjà proches et en éloignant les moins proches. 

### Cosinus Similarity Loss

Nous avons également décidé d'utiliser le crowdsourcing pour améliorer notre modèle. L'idée est d'utiliser l'avis des utilisateurs pour fine-tuner le modèle. Comme pour la Triplet Loss, on rapproche les synopsis et les requêtes que l'utilisateur jugent similaires et on éloigne les moins proches. 

Pour cela, on utilise la [*Cosine Similarity Loss*](https://www.sbert.net/docs/package_reference/losses.html#cosinesimilarityloss). On récupère l'information des utilisateurs grâces aux avis ( :+1: et :-1: ), ce qui nous donne des informations ayant la structure suivante : 

```python
(['synopsis', 'query'], label)
```

où le label dépend de l'avis de l'utilisateur. Nous avons arbitrairement choisi de fixer les labels suivants : 

- :+1: = 0.2
- :-1: = 1.5

Ces valeurs ont été choisies après observation des données, pour que les labels aient des valeurs légérement en dessus et en dessous des maximums et des minimums du calcul de la distance cosinus.

L'avantage de la Cosinus Similarity Loss par rapport à la Triplet Loss est qu'il n'est pas nécessaire d'avoir un exemple négatif pour un synopsis donné pour pouvoir finetuner sur un exemple positif et inversement. 

### Automatisation du processus

Etant donné que l'on finetune sur des reviews d'utilisateurs, il est favorable d'automatiser le lancement du finetuning. Pour ce faire, nous avons simplement utilisé le module `time` pour créer un décorateur qui impose une condition au lancement de la fonction de finetuning. Si la fonction de finetuning a déjà été lancée il y a moins d'une semaine, alors rien ne se passe. Sinon, le fine tuning est lancé, l'ancien modèle est archivé et les nouveaux embeddings du corpus sont générés.

>[!note]
>Pour l'instant les anciens modèles sont automatiquement archivés. Cette méthode ne sera plus utilisable telle quelle par la suite, les modèles étant trop volumineux pour que cela fonctionne à long terme.

Les fonctions d'automatisation peuvent être retrouvées ici : `JADe_project/app/src/scripts/utils.py`.