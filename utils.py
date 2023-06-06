from os import listdir, remove

def flush_dir(dir):
    for filename in listdir(dir):
        remove(dir + filename)