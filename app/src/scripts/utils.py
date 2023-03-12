import time
import shutil
import os

def stash(source_path, destination_path):
    shutil.move(source_path, destination_path)
    return destination_path

def get_new_name(filename,folder_path):
    files = os.listdir(folder_path)
    id = sorted(files, key = lambda x : int(x.split("_")[1:]), reverse=True)[0]
    if "\\" in folder_path:
        return f"{folder_path}\\{filename}_v{id}"
    return f"{folder_path}/{filename}_v{id}"

def set_timer(func):
    def wrapper_set_timer(*args, **kwargs):
        start_time = time.time()
        with open(".times", "a") as f:
            f.write(f"{start_time}\n")
        func(*args, **kwargs)
    return wrapper_set_timer


def check_time(duration):
    def inter_check_time(func):
        def wrapper_check_time(*args, **kwargs):
            with open(".times", "r") as f:
                then = float(f.readlines()[-1].strip())
            now = time.time()
            time_since = now - then
            if time_since >= duration:
                func(*args, **kwargs)
        return wrapper_check_time
    return inter_check_time


@set_timer
def example(x):
    print(x)

@check_time(duration = 604800)
def example(stuff):
    print(stuff)