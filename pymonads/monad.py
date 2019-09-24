from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Any

from pymonads.applicative import Applicative
from pymonads.functor import Functor
from pymonads.utils import compose

T = TypeVar('T', covariant=True)
T_co = TypeVar('T_co', covariant=True)
U_co = TypeVar('U_co', covariant=True)

A = TypeVar('A')
B = TypeVar('B')

class Monad(Applicative, Generic[T_co], metaclass=abc.ABCMeta):
    """Base class for Monad implementations"""

    @abc.abstractmethod
    def flat_map(self, func: Callable[[T_co], Monad]) -> Monad:
        """Monadic bind or the `>>=` operator."""

    def __or__(self, func: Callable[[T_co], Monad[U_co]]) -> Monad[U_co]:
        """Allows the use of `|` to call flat_map."""
        return self.flat_map(func)

    def __rshift__(self, mb: Monad[U_co]) -> Monad[U_co]:
        """Allows the use of `>>` to sequence operations, ignoring the first arg."""
        def return_mb(mb):
            return mb
        return self.flat_map(return_mb)

    def map(self, func: Callable[[T_co], U_co]) -> Monad[U_co]:
        """Map over values in some monad."""
        def a_to_mb(some_a: A) -> Monad[T_co]:
            return compose(self.pure, func)(some_a)

        return self.flat_map(a_to_mb)
