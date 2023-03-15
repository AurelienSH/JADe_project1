## Les autres pistes envisagées 

### L'augmentation des données

#### Backtranslation

L'idée était ici d'augmenter les données en traduisant les synopsis dans une langue cible pour ensuite les traduire à nouveau dans la langue source.
Les modèles que nous avons trouvé n'ont pas donné des résultats assez différents des synopsis originaux pour justifier le coût en énergie et en temps.
Il serait intéressant de voir d'autres options permettant de le faire de façon plus raisonnable et/ou efficace.

#### Summarization

Nous avions songé à augmenter les données en partant d'une bdd de la partie "Plot" et "Summary" de tous les articles wikipedia en possédant et en finetunant un générateur de résumé automatique qui partirait de la concaténation des données de wikipédia vers nos synopsis.
Le but était ici de pouvoir réellement générer des synopsis automatiquement à partir des résumés, les résumés étant plus nombreux on aurait donc une plus large quantité de donnée.
De la meme façon nous avions penser à le faire à partir des oeuvres entières.
Il serait d'ailleurs intéressant d'imaginer les embeddings générables à partir de cette tâche également.
Encore une fois, il n'a pas été possible de l'implémenter pour l'instant, dû à des machines trop peu performantes pour donner des résultats utilisables qui pourrait générer autre chose que du bruit.

### Pour le système

#### Classification avec BERT

Nous avons envisagé à un moment d'utiliser un système de classification pour générer les recommandations. L'idée était d'entrainer un classifieur basé sur un transformer (tel que BERT) afin d'essayer de classer des synopsis en titre de film. 
L'idée étant ensuite de ne pas espérer que le classifieur réussise à classer les films, la tâche étant de donner une liste de recommandation, il aurait été intéressant de voir ce que le classifieur aurait pu générer.
Ce qui paraissait intéressant ici était l'idée que le classifieur pourrait se baser sur des mesures plus intéressantes qu'un  calcul de distance. Malheureusement notre seul essai n'a pas encore pu aboutir à un modèle dû à un entraînement trop coûteux.

#### Doc2Vec

Nous avons considéré, au début, d'utiliser Doc2Vec pour obtenir les embeddings de nos documents. Néanmoins, nous avons préféré l'option des Sentences Transformers car nous pouvions les personnaliser avec le fine-tuning. Un tutoriel sur le fonctionnement de Doc2Vec est disponible dans le dossier `system_test` : `demo_transformers_and_doc2vec.ipynb`

####

## Autres Idées

On pourrait envisager d'enrichir encore la base de donnée de nouveaux synopsis, et de faire fonctionner l'augmentation automatique de données. 

De plus, pour le moment, notre corpus est exclusivement en anglais. Il pourrait être envisageable d'en faire un système multilingue. 
