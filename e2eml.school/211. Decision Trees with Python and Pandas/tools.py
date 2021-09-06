import pickle
import matplotlib.pyplot as plt


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


def custom_scatter(x, y):
    """
    Parameters
    -----------
    x, y: iterable of floats
        x and y need to be of the same length
    """

    plt.plot(
        x, y,
        color='black',
        marker=".",
        linestyle='none',
        alpha=.1
    )
    plt.show()
