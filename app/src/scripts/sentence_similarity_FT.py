##############################################################
#                                                            #
#                     IMPORTATION DES MODULES                #
#                                                            #
##############################################################

import csv
from collections import namedtuple
import random

# Fine-tuning
from torch.utils.data import DataLoader
from sentence_transformers.readers import InputExample

from sentence_transformers import SentenceTransformer,  SentencesDataset, LoggingHandler, losses

# Similarité
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances

from sentence_similarity import read_corpus

def main():
    
    # Définir un named tuple pour représenter des coordonnées géographiques
    Query_FT = namedtuple('Query_FT', ['anchor_text', 'positive_text','negative_text'])
    
    pass
    
if __name__ == "__main__":
    main()