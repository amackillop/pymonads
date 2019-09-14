from typing import TypeVar

A = TypeVar('A')

def const(value: A, _) -> A:
    """ Simply returns it's first argument"""
    return value
