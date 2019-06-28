# coding: utf-8
""" Utility functions for ibflex """
import itertools


def identity_func(x):
    return x


def all_equal(iterable):
    """Returns True if all the elements are equal to each other

    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    g = itertools.groupby(iterable)
    return next(g, True) and not next(g, False)
