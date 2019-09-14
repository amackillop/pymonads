from typing import TypeVar

A = TypeVar('A')

def identity(value: A) -> A:
    """The identity function"""
    return value

def const(value: A, _) -> A:
    """ Simply returns it's first argument"""
    return value
