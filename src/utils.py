import os

def get_path(f):
    dirname = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(dirname, f).replace('/', '\\')