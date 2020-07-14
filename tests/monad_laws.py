"""
The Monad Laws.
"""

from typing import TypeVar, Callable

from pymonads.monad import Monad
from pymonads.utils import identity, compose

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def monad_respects_left_identity(monad: Monad[A], value: A, func: Callable[[A], B]) -> bool:
    return monad.pure(value).flat_map(func) == func(value)

def monad_respects_right_identity(monad: Monad[A], value: A, func: Callable[[A], B]) -> bool:
    return monad.flat_map(monad.pure) == monad

def monad_respects_associativity(monad: Monad[A], f: Callable[[A], Monad[B]], g: Callable[[B], Monad[C]]) -> bool:
    return monad.flat_map(f).flat_map(g) == monad.flat_map(lambda x: (f(x).flat_map(g)))
