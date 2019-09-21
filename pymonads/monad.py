from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Generic, TypeVar, NewType, Callable

from pymonads.applicative import Applicative
from pymonads.functor import Functor
from pymonads.utils import compose

T = TypeVar('T', covariant=True)
T_co = TypeVar('T_co', covariant=True)

A = TypeVar('A')
B = TypeVar('B')

class Monad(Applicative, Generic[T_co], metaclass=abc.ABCMeta):
    """Base class for Monad implementations"""

    @abc.abstractmethod
    def flat_map(self, func) -> Monad[T_co]:
        """Monadic bind or the `>>=` operator."""

    def __or__(self, func: Callable[[A], Monad[T_co]]) -> Monad[T_co]:
        """Allows the use of `|` to call flat_map."""
        return self.flat_map(func)

    def __rshift__(self, mb: Monad[B]) -> Monad[T_co]:
        """Allows the use of `>>` to sequence operations, ignoring the first arg."""
        def return_mb(mb):
            return mb
        return self.flat_map(return_mb)

    def map(self, func: Callable[[A], T_co]) -> Monad[T_co]:
        """Map over values in some monad."""
        def a_to_mb(some_a: A) -> Monad[T_co]:
            return compose(self.pure, func)(some_a)

        return self.flat_map(a_to_mb)
