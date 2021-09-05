import pickle

def restore(filename):
    data = None
    with open(filename) as dfile
        data = pickle.load(dfile)
    return data

def store(dicts, filename, verbose=True):
    with open(filename, 'wb') as dfile:
        pickle.dump(dicts, dfile)
    if verbose:
        print("Data stored in \'{filename}\'").format(filename=filename)

