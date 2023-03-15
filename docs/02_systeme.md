# Système 

Cette section décrit le système utiliser pour faire foncitonner :clapper: *SynSearch*

utilisation des sentences transformers pour créer des embeddings de documents (exploration de doc2vec et classification également)

Toutes les informations utilisées proviennent de [Hugging Face :hugs:](https://huggingface.co/) et de [SBERT](https://www.sbert.net/index.html).

## Modèle choisi 

Nous avons choisi d'utiliser des Sentences Transformers pour avoir une représentation en vecteur de nos données. Plus précisément, nous avons choisi le modèle **[all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)**. Le choix de se modèle s'est fait de façon un aléatoire, nous n'avons pas défini de critère de selection. 

Une fois le modèle choisi, nous l'avons utiliser pour encoder nos documents textuelles, pour en avoir une représentation numérique (sous forme de vecteur). 

Nous avons utiliser le même modèle pour encoder la requête de l'utilisateur.

Cela permet ainsi de calculer la distance (cosinus) entre la requête d'un utilisateur et le synopsis d'un film. Plus la distance est faible (c'est à dire se rapproche de 0), plus la requête et le synopsis sont proches. 

Ainsi, on suggère les cinq films les plus proches de la requête à l'utilisateur. 

Nous avons choisi d'utiliser des Sentences Transformers car ces transformers sont une référence dans l'état de l'art pour les embeddings de documents. De plus, ils sont faciles à utiliser, et rapide à fine-tuner. Pour voir les autres options que l'on a envisagé, c'est par [là](methodologie.md#pour-le-système)

## Fine tuning 
 
Plusieurs pistes pour le fine-tuning étaient possibles, mais elles demandaient toutes un autre format de données que celui que nous avions. Nous avons retenus deux fonctions de pertes pour fine-tuner notre modèle :
- La Triplet Loss
- La Cosinus Similarity Loss

### Triplet Loss


Les requêtes des utilisateurs ne sont pas vraiment semblables au synopsis de films. C'est pour cela qu'il fallait qun fine-tuning de notre modèle, pour ainsi prendre en comtpe le format des requêtes des utilisateur. Pour utiliser la Triplet Loss, il faut un format de dataset particulier : 
- Anchor
- Positiv
- Negativ <br>

Ici, *Anchor* correspond à un synopsis, *Positiv* à une requête correspondant au synopsis et *Negativ* une requete ne correspondant pas au synopsis. 
Ainsi, on peut fine-tuner notre modèle pour que le format des requêtes des utilisateurs soit pris en compte par le modèle lors du calcul de similarité. 

Pour avoir ce format de dataset, nous avons [augmenté manuellement nos données](data.md#augmentation-manuelle--queries). 

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
- :+1: = 0.4
- :-1: = 1.6 <br>
Ces valeurs ont été choisi après observation des données, pour que les labels aient des valeurs légérement en dessus et en dessous des maximum et des minimums du calcul de la distance cosinus. 

>[!Warning]
> explication de l'automatisation
