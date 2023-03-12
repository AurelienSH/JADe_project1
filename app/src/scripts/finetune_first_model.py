##############################################################
#                                                            #
#                     IMPORTATION DES MODULES                #
#                                                            #
##############################################################

import pickle
import csv
from collections import namedtuple
import random

from sentence_transformers import SentenceTransformer, InputExample, losses, SentencesDataset
from torch.utils.data import DataLoader

from preprocessing import make_embeddings_corpus, read_corpus

#########################################################

def main():
    
    # Chargement du corpus augmenté manuellement
    with open("../../../Data/movie_synopsis_augmented.csv", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            
            # Récupération des données sous la forme d'une liste de listes
            corpus_augmented = [[line["synopsis"], line["title"], line["query"]] for line in csv_reader]
            
    # Définir un named tuple pour représenter les oeuvres et leurs queries
    Query_FT = namedtuple("Query_FT", ["synopsis", "pos_query","neg_query"])

    data_for_fine_tuning = []

    for synopsis, title, query in corpus_augmented:

        if query != "": # S'il a bien une query pour ce film
            
            neg = random.choice(corpus_augmented)[0] # Synopsis d'une oeuvre au hasard dans corpus

            if neg != synopsis: # Si ce n'est pas la même oeuvre
                
                data_for_fine_tuning.append(Query_FT(synopsis=synopsis, pos_query=query, neg_query=neg))

            else : 
                neg = random.choice(corpus_augmented)[0] # On re-prend un synopsis au hasard
                data_for_fine_tuning.append(Query_FT(synopsis=synopsis, pos_query=query, neg_query=neg))

    # Chargement du modèle
    model = SentenceTransformer(model_name_or_path='sentence-transformers/all-MiniLM-L6-v2')

    # Mise en forme du corpus d'entrainement
    train_examples = [InputExample(texts=[anchor_text, pos_query, neg_query]) for anchor_text, pos_query, neg_query in data_for_fine_tuning] 
    train_dataset = SentencesDataset(train_examples, model)
    train_dataloader = DataLoader(train_dataset, shuffle=True) #, batch_size=32

    # Entraînement du modèle
    train_loss = losses.TripletLoss(model=model)
    model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=10)
    
    corpus = read_corpus("../../../Data/movie_synopsis.csv")

    # Création des embeddings avec le modèle fine-tuné
    embeddings_corpus = make_embeddings_corpus(corpus, model=model)

    # Sauvegarde des embeddings dans un fichier pickled
    with open("../../embeddings/embeddings_FT_corpus_movie", "wb") as embedding_corpus_file:
        pickle.dump(embeddings_corpus, embedding_corpus_file)
        
    # Sauvegarde du modèle fine-tuné
    model.save("../../models/sentence_similarity_model_FT")
    
if __name__=="__main__":
    main()