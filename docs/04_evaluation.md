# Evaluation 

## Quantitative

Script et données : `JADe_project1/eval`

Pour un premier essai d'évaluation, nous avons songé à utiliser la même méthodolige qu'utilise Doc2Vec : Nous avons cherché à savoir si le document le plus proche d'un document cible était lui même. 

Nous avons ainsi évalué :
1. le modèle avant fine-tuning, en utilisant les synopsis. 
2. le modèle après fine-tuning, en utilisant les requêtes.

Dans les deux cas, le résultats était de 100% de réussite, ce qui est attendu.

Dans un deuxième temps, nous avons procéder à la rédaction de trois styles différents 

Les trois styles que nous avons choisi d’évaluer sont les suivants :

Description :
Une description détaillée d’un film sans se préoccuper de la forme
exemple : "A movie in which we follow a life's guy though the good and the bad moment. The guy has a very busy life, doing a lot of new stuff and living a lot of adventure. He lives during the big moment of the United States. There is a love story though the entire movie but the guy never get the girl."


Queries :
Une demande en langage naturel comme on pourrait la formuler à un interlocuteur 
exemple : "i'm looking for a movie about a girl pretending to be a man so she can replace her father in the army. the reason she's doing this is because her father is very sick and she was afraid he wouldn't come back in one piece. china is saved thanks to her, even thought when they discovered she wasn't a girl, people thought she was a liability."


Synopsis :
Un court texte rédigé dans le style de ce que l’on pourrait trouver à l’arrière d’une VHS
exemple : "A young man is having a hard time chosing is allegiances. His mentor will try and help him during the ongoing war, but it will be hard for him to choose. In the end will he be able to make the right sacrifices ?"

Voilà un tableau des scores obtenus :

|      | Description | Queries | Synopsis |
|------|-------------|---------|----------|
| noFT | 0.22        | 0.47    | 0.47     |
| FT   | 0.22        | 0.47    | 0.52     |

Sur de très courts exemples, c’est assez rassurant de déjà voir un peu d’amélioration, qui plus est dans le style qui correspond le plus à l’ambition du projet.
Il sera intéressant de voir la manière dont ces scores pourraient évoluer après plusieurs fine tuning sur des données réelles.

## Qualitative 

Il est notable qu'au court de l'évaluation quantitative ciblée, on remarque que parfois même si le film en question n’est pas dans la liste les films est très convaincante. Souvent, si le film se trouve être dans une saga, on retrouve au moins un des autres opus. Autrement, on obtient souvent des résultats de films du même studio (surtout pour Disney Pixar).

-> crowdsourcing 
Une manière d'évaluer notre modèle est d'utiliser les avis des utilisateurs grâce au crowdsourcing

-> manuellement 
En attendant, nous avons utiliser nous même notre API pour donner nos avis. 