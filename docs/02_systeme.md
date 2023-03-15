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
 
Plusieurs pistes pour le finetuning étaient possibles. Toutefois, elles demandaient toutes un autre format de données que celui que nous avions. Nous avons retenus deux fonctions de pertes pour fine-tuner notre modèle :

- La Triplet Loss
- La Cosinus Similarity Loss

### Triplet Loss


Les requêtes des utilisateurs ne sont pas vraiment semblables au synopsis de films. C'est pour cela qu'il fallait qun fine-tuning de notre modèle, pour ainsi prendre en comtpe le format des requêtes des utilisateur. Pour utiliser la Triplet Loss, il faut un format de dataset particulier : 
- Anchor
- Positiv
- Negativ <br>

Ici, *Anchor* correspond à un synopsis, *Positiv* à une requête correspondant au synopsis et *Negativ* une requete ne correspondant pas au synopsis. 
Ainsi, on peut fine-tuner notre modèle pour que le format des requêtes des utilisateurs soit pris en compte par le modèle lors du calcul de similarité. 

Pour avoir ce format de dataset, nous avons [augmenté manuellement nos données](01_data.md#augmentation-manuelle). 

Voici un exemple de données obtenues :

| id | synopsis | title          | **query**                                                          |
|----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|-----------------------------------------------------------------|
| 0  | It's Ted the Bellhop's first night on the job...and the hotel's very unusual guests are about to place him in some outrageous predicaments. It seems that this evening's room service is serving up one unbelievable happening after another.                                                                                                                                                                    | Four Rooms     | **I want to watch a quirky and chaotic comedy movie**              |
| 1  | While racing to a boxing match, Frank, Mike, John and Rey get more than they bargained for. A wrong turn lands them directly in the path of Fallon, a vicious, wise-cracking drug lord. After accidentally witnessing Fallon murder a disloyal henchman, the four become his unwilling prey in a savage game of cat & mouse as they are mercilessly stalked through the urban jungle in this taut suspense drama | Judgment Night | **I'm in the mood for an intense and action-packed thriller movie** |


En suivant la documentation, nous avons utiliser la [*Triplet Loss*](https://www.sbert.net/docs/package_reference/losses.html#tripletloss) pour fine-tuner notre modèle. 

Cette méthode a permis d'améliorer les suggestions en rapprochant les requêtes et les synopsis déjà proches et en éloignant les moins proches. 


### Cosinus Similarity Loss

Nous avons également décidé d'utiliser le crowdsourcing pour améliorer notre modèle. L'idée est d'utiliser l'avis des utilisateurs pour fine-tuner le modèle : on rapproche les synospsis et les requêtes que l'utilisateur jugent similaires et inversement. 

Pour cela, on utilise la [*Cosine Similarity Loss*](https://www.sbert.net/docs/package_reference/losses.html#cosinesimilarityloss). 
On récupère l'information des utilisateurs grâces aux avis ( :+1: et :-1: ), ce qui nous donne des informations ayant la structure suivante : 

```python
(['synopsis', 'query'], label)
```

où le label dépend de l'avis de l'utilisateur. Nous avons arbitrairement choisi de fixer les labels suivants : 
- :+1: = 0.2
- :-1: = 1.5 <br>
Ces valeurs ont été choisi après observation des données, pour que les labels aient des valeurs légérement en dessus et en dessous des maximum et des minimums du calcul de la distance cosinus.

### Automatisation du processus

Dans notre cas, il est favorable d'automatiser le lancement du fine tuning.
Pour ce faire nous avons simplement utiliser le module time pour créer un décorateur qui impose une condition au lancement de la fonction de finetuning :
Si la fonction de finetuning a déjà été lancée il y a moins d'une semaine, alors rien ne se passe, sinon, le fine tuning est lancé l'ancien modèle archivé et les nouveaux embeddings générés.

Pour l'instant les anciens modèles sont automatiquement archivés, mais cette méthode ne sera plus utilisée telle quelle par la suite, les modèles étant trop volumineux pour que cela fonctionne à long terme.

Les fonctions d'automatisation peuvent etre retrouvées ici : `JADe_project/app/src/scripts/utils.py`
