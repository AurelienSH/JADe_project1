## Les autres pistes envisagées 

### L'augmentation des données

#### Backtranslation

L'idée était ici d'augmenter les données en traduisant les synopsis dans une langue cible pour ensuite les traduire à nouveau dans la langue source. Les modèles que nous avons trouvé n'ont pas donné des résultats assez différents des synopsis originaux pour justifier le coût en énergie et en temps. Il serait intéressant de voir d'autres options permettant de le faire de façon plus raisonnable et/ou efficace. Peut-être en masquant des mots. 

#### Summarization

Nous avions songé à augmenter les données en partant d'une BDD de la partie "Plot" et "Summary" de tous les articles Wikipédia ([WikiPlots](https://github.com/markriedl/WikiPlots)) et en finetunant un générateur de résumé automatique qui partirait de la concaténation des données de wikipédia vers nos synopsis.

Nous avons constitué ce-dit corpus avec le script `JADe_project1/Data/scripts/make_dataset_imdb_wiki.ipynb`. Il se trouve dans `JADe_project1/Data/uldv_wiki_corpus.csv`. Il associe les longs "plots" Wikipédia à son court synopsis IMDB. Ci-dessous un extrait de ce corpus : 

| document | summary |
|---|---|
| Old Major, the old boar on the Manor Farm, summons the animals on the farm together for a meeting, during which he refers to humans as ""enemies"" and teaches the animals a revolutionary song called ""Beasts of England"".[...] However, the ideals which Snowball discussed, including stalls with electric lighting, heating and running water are forgotten, with Napoleon advocating that the happiest animals live simple lives.In addition to Boxer, many of the animals who participated in the Revolution are dead, as is Farmer Jones, who died in another part of England.The pigs start to resemble humans, as they walk upright, carry whips, and wear clothes.The Seven Commandments are abridged to a single phrase: ""All animals are equal but some animals are more equal than others"".Napoleon holds a dinner party for the pigs and local farmers, with whom he celebrates a new alliance.He abolishes the practice of the revolutionary traditions and restores the name ""The Manor Farm"".As the animals look from pigs to humans, they realise they can no longer distinguish between the two. | A successful farmyard revolution by the resident animals vs. the farmer goes horribly wrong when corrupt pigs hijack it for their personal gain. |
| Alex is a 15-year-old living in near-future dystopian England who leads his gang on a night of opportunistic, random ""ultra-violence"".Alex's friends (""droogs"" in the novel's Anglo-Russian slang, 'Nadsat') are Dim, a slow-witted bruiser who is the gang's muscle; Georgie, an ambitious second-in-command; and Pete, who mostly plays along as the droogs indulge their taste for ultra-violence. [...] In the final chapter, Alex finds himself halfheartedly preparing for yet another night of crime with a new gang (Lenn, Rick, Bully).After a chance encounter with Pete, who has reformed and married, Alex finds himself taking less and less pleasure in acts of senseless violence.He begins contemplating giving up crime himself to become a productive member of society and start a family of his own, while reflecting on the notion that his own children will be just as destructive as he has been, if not more so. | In a near-future Britain, young Alexander DeLarge and his pals get their kicks beating and raping anyone they please. When not destroying the lives of others, Alex swoons to the music of Beethoven. The state, eager to crack down on juvenile crime, gives an incarcerated Alex the option to undergo an invasive procedure that'll rob him of all personal agency. In a time when conscience is a commodity, can Alex change his tune? |

Le but était ici de pouvoir réellement générer des synopsis automatiquement à partir de résumés. Les résumés de films étant plus faciles à trouver que des synopsis multiples pour une même oeuvre donnée, on aurait donc pu avoir une plus large quantité de données. De la meme façon nous avions penser à le faire à partir des oeuvres entières : peut-être en prenant les scripts des films ? 

Il serait d'ailleurs intéressant d'imaginer les embeddings générables à partir de cette tâche également.

Encore une fois, il n'a pas été possible de l'implémenter pour l'instant, dû à des machines trop peu performantes pour donner des résultats utilisables qui pourrait générer autre chose que du bruit. 

### Expansion de l'API

On pourrait envisager d'enrichir encore la base de données de nouveaux synopsis. Par ailleurs, on pourrait étendre notre API aux livres, aux fanfictions, aux séries ou à toute autre type d'oeuvre. 

De plus, pour le moment, notre corpus est exclusivement en anglais. Il pourrait être envisageable d'en faire un système multilingue. 

### Pour le système

#### Classification avec BERT

Nous avons envisagé à un moment d'utiliser un système de classification pour générer les recommandations. L'idée était d'entrainer un classifieur basé sur un transformer (tel que BERT) afin d'essayer de classer des synopsis en titre de film. Il n'était pas nécessaire que le classifieur réussise à classer les films. La tâche étant de donner une liste de recommandations, il aurait été intéressant de voir ce que le classifieur aurait pu générer.

Ce qui paraissait intéressant ici était l'idée que le classifieur pourrait se baser sur des mesures plus intéressantes qu'un  calcul de distance. Malheureusement notre seul essai n'a pas encore pu aboutir à un modèle dû à un entraînement trop coûteux.

#### Doc2Vec

Nous avons considéré, au début, d'utiliser Doc2Vec pour obtenir les embeddings de nos documents. Néanmoins, nous avons préféré l'option des Sentences Transformers car nous pouvions les personnaliser avec le finetuning. Un tutoriel sur le fonctionnement de Doc2Vec est disponible dans le dossier `system_test/demo_transformers_and_doc2vec.ipynb`