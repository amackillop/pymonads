"""
The Functor Laws.
"""

from typing import TypeVar, Callable

from pymonads.functor import Functor
from pymonads.utils import identity, compose

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def functor_preserves_identity_morphisms(functor: Functor[int]) -> bool:
    return functor.fmap(identity) == identity(functor)

def functor_preserves_composition_of_morphisms(functor: Functor, f: Callable[[B], C], g: Callable[[A], B]) -> bool:
    return functor.fmap(compose(f, g)) == functor.fmap(g).fmap(f)
