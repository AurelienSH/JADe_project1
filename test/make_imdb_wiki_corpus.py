import re
import csv
import pickle

def main():
    
    ##############################################################
    #                                                            #
    #                    LECTURE DES FICHIERS                    #
    #                                                            #
    ##############################################################
    
    # Fichiers avec les données
    imdb_synopsis_file = "../Data/movie_synopsis.csv"
    wiki_plots_file = "../Data/plots/plots"
    wiki_plots_titles_file = "../Data/plots/titles"

    # Lecture du fichier avec les synopsis IMDB
    with open(imdb_synopsis_file, "r", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        # Création d'un dictionnaire {title: synopsis_IMDB}
        imdb_data = {row["title"].lower(): row["synopsis"] for row in csv_reader}
        
    # Lecture du fichier avec les plots détaillés Wikipédia
    with open(wiki_plots_file, "r", encoding="utf-8") as f:
        l = f.readline()
        plots = []
        temp_plot = [] # Un plot peut s'étaler sur plusieurs lignes
        while l:
            if l == "<EOS>\n": # Fin du plot
                plots.append(temp_plot)
            else:
                temp_plot.append(l.strip())
            l = f.readline()
            
    # Lecture du fichier avec les titres correspondants aux plots de Wikipédia
    with open(wiki_plots_titles_file, "r", encoding="utf-8") as f:
        wiki_plots_titles = []
        l = f.readline()
        while l :
            title = re.sub(r"\((\w+|\d+)\)", "", l) # Suppression des infos entre parenthèses (ex : "(movie)", "(1998)", ...)
            wiki_plots_titles.append(title.lower().strip()) # Tout en minuscules et suppression des trailing spaces
            l = f.readline()

    ##############################################################
    #                                                            #
    #                    CREATION DE TUPLES LIANT                #
    #                  UNE OEUVRE A SON SYNOPSIS IMDB            #
    #                      ET SON PLOT WIKIPEDIA                 #
    #                                                            #
    ##############################################################

    # Tuples avec le titre de l'oeuvre, son plot détaillé wikipédia et le synopsis IMDB
    oeuvres = [(title, plot, imdb_data.get(title, "")) for title, plot in zip(wiki_plots_titles, plots)]

    # Suppression de tous les oeuvres pour lesquelles on a pas le synopsis IMDB
    oeuvres_imdb_not_empty = [oeuvre for oeuvre in oeuvres if oeuvre[2]!=""]

    # Sauvegarde du corpus dans un fichier pickled
    with open("../Data/imdb_wiki_corpus_pickled", "wb") as corpus_file:
        pickle.dump(oeuvres_imdb_not_empty, corpus_file)

if __name__ == "__main__":
    main()