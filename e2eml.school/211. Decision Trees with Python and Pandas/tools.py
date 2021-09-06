import pickle

def restore(filename):
    data = None
    with open(filename, 'rb') as dfile:
        data = pickle.load(dfile)
    return data

def store(dicts, filename, verbose=True):
    with open(filename, 'wb') as dfile:
        pickle.dump(dicts, dfile)
    if verbose:
        print(f"Data stored in \'{filename}\'")

