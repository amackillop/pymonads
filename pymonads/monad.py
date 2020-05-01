from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, Any

from pymonads.applicative import Applicative
from pymonads.utils import compose

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
U_co = TypeVar('U_co', covariant=True)

A = TypeVar('A')
B = TypeVar('B')

class Monad(Applicative[T_co], ABC):
    """Base class for Monad implementations"""

    @abstractmethod
    def flat_map(self, func: Callable[[A], Monad[B]]) -> Monad[B]:
        """Monadic bind or the `>>=` operator."""

    def __or__(self, func: Callable[[A], Monad[B]]) -> Monad[B]:
        """Allows the use of `|` to call flat_map."""
        return self.flat_map(func)

    def __rshift__(self, mb: Monad[B]) -> Monad[B]:
        """Allows the use of `>>` to sequence operations, ignoring the first arg."""
        def return_mb(mb):
            return mb
        return self.flat_map(return_mb)

    def map(self, func: Callable[[A], B]) -> Monad[B]:
        """Map over values in some monad."""
        def a_to_mb(some_a: A) -> Monad[B]:
            return compose(self.pure, func)(some_a)

        return self.flat_map(a_to_mb)
