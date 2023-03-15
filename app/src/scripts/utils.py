import time
from shutil import move
import os
from os import path

def get_new_name(filename: str, folder_path: str):
    """
    Fonction générant le nom de version d'un fichier lors de son archivage
    Args:
        filename (str)
        folder_path (str)

    Returns:
        str
    """

    # Vérification de l'existence du dossier d'archivage, s'il n'existe pas il est créé, et la fonction renvoie que le fichier et la première version
    if not path.exists(folder_path):
        os.mkdir(folder_path)
        return f"{folder_path}/{filename}_v1"

    # Génération du numéro de version
    files = os.listdir(folder_path)
    id = int(sorted(files, key=lambda x: int(x.split("_")[-1][1:]), reverse=True)[0].split("_")[-1][1:])+1

    # Condition dans le cas ou un utilisateur utiliserait le formattage d'arborescence de windows
    if "\\" in folder_path:
        return f"{folder_path}\\{filename}_v{id}"
    return f"{folder_path}/{filename}_v{id}"


def set_timer(func):
    """
    Fonction ajoutant le moment actuel dans un fichier de sauvegarde, permettant de générer un timer depuis cet instant
    Returns:
        start_time (float)
    """
    start_time = time.time()
    with open(f".times_{func.__name__}", "a") as f:
        f.write(f"{start_time}\n")
    return start_time


def check_time(duration: int =604800, repeat : bool = False):
    """
    Décorateur permettant de lancer une fonction uniquement si le nombre de seconde "duration" s'est écoulé depuis sa dernière utilisation
    Args:
        duration (int) : temps en seconde jusqu'à l'autorisation à une prochaine éxecution
        repeat (bool) : si True, remettra le timer à jour automatiquement après chaque éxecution de la fonction
    """
    def inter_check_time(func):
        def wrapper_check_time(*args, **kwargs):
            print(args, kwargs)
            if path.exists(f".times_{func.__name__}"):
                with open(f".times_{func.__name__}", "r") as f:
                    then = float(f.readlines()[-1].strip())
            else:
                then = 0
            now = time.time()
            time_since = now - then
            if time_since >= duration:
                func(*args, **kwargs)
                if repeat:
                    set_timer(func)
        return wrapper_check_time

    return inter_check_time

# Exemple de définition de fonction avec le décorateur check_time
# @check_time(duration = 180)
# def example(stuff):
#    print(stuff)