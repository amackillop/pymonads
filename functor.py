from __future__ import annotations

import abc
from functools import partial
from typing import Generic, TypeVar, Callable

from utils import const

T_co = TypeVar('T_co', covariant=True)

A = TypeVar('A')
B = TypeVar('B')

class Functor(Generic[T_co], metaclass=abc.ABCMeta):
    """docstring"""

    @abc.abstractmethod
    def map(self, func: Callable[[A], B]) -> Functor[B]:
        """fmap"""

    def map_replace(self, value: A):
        """<$"""
        return self.map(partial(const, value))
