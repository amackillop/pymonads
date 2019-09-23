"""
The Applicative Functor Laws.
"""

from typing import TypeVar, Callable

from pymonads.applicative import Applicative 
from pymonads.utils import identity, compose

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def test_applicative_identity_law(either):
    assert either.amap(pure(identity)) == either