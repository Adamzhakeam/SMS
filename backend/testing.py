import os
from pprint import pprint

def directory_structure(root_dir):
    structure = {}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        path = dirpath.split(os.sep)
        subtree = {d: {} for d in dirnames}
        files = {f: None for f in filenames}
        
        parent = reduce(lambda d, key: d.setdefault(key, {}), path[1:], structure)
        parent.update(subtree)
        parent.update(files)
    
    return structure

if __name__ == "__main__":
    root_directory = "."  # Change this to the root directory you want to list
    structure = directory_structure(root_directory)
    pprint(structure)
