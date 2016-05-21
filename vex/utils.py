__author__ = 'adalekin'


def get_in_dict(dictionary, key):
    return reduce(lambda d, k: d[k], key, dictionary)


def set_in_dict(dictionary, key, value):
    get_in_dict(dictionary, key[:-1])[key[-1]] = value