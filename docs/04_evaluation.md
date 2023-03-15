# Evaluation 

## Quantitative

(où trouver le script).

Pour un premier essai d'évaluation, nous avons songé à utiliser la même méthodolige qu'utilise Doc2Vec : Nous avons cherché à savoir si le document le plus proche d'un document cible était lui même. 

Nous avons ainsi évalué :
1. le modèle avant fine-tuning, en utilisant les synopsis. 
2. le modèle après fine-tuning, en utilisant les requêtes.

Dans les deux cas, le résultats était de 100% de réussite, ce qui est attendu.

Dans un deuxième temps, nous avons procéder à la rédaction de trois styles différents 

Les trois styles que nous avons choisi d’évaluer sont les suivants :

Description :
Une description détaillée d’un film sans se préoccuper de la forme

Queries :
Une demande en langage naturel comme on pourrait la formuler à un interlocuteur 

Synopsis :
Un court texte rédigé dans le style de ce que l’on pourrait trouver à l’arrière d’une VHS

Voilà un tableau des scores obtenus :

Sur de très courts exemples, c’est assez rassurant de déjà voir un peu d’amélioration, qui plus est dans le style qui correspond le plus à l’ambition du projet.
Il sera intéressant de voir la manière dont ces scores pourraient évoluer après plusieurs fine tuning sur des données réelles.

## Qualitative 

Il est notable qu'au court de l'évaluation quantitative ciblée, on remarque que parfois même si le film en question n’est pas dans la liste les films est très convaincante. Souvent, si le film se trouve être dans une saga, on retrouve au moins un des autres opus. Autrement, on obtient souvent des résultats de films du même studio (surtout pour Disney Pixar).

-> crowdsourcing 
Une manière d'évaluer notre modèle est d'utiliser les avis des utilisateurs grâce au crowdsourcing

-> manuellement 
En attendant, nous avons utiliser nous même notre API pour donner nos avis. 