from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Generic, TypeVar, NewType, Callable

from applicative import Applicative
from functor import Functor

from utils import compose

T = TypeVar('T', covariant=True)
T_co = TypeVar('T_co', covariant=True)

A = TypeVar('A')
B = TypeVar('B')

class Monad(Applicative, Generic[T_co], metaclass=abc.ABCMeta):
    """Base class for Monad implementations"""

    @abc.abstractmethod
    def flat_map(self, func: Callable[..., Monad[B]]) -> Monad[B]:
        """m a -> (a -> m b) -> m b"""

    def __or__(self, func: Callable[..., Monad[B]]) -> Monad[B]:
        return self.flat_map(func)

    def __rshift__(self, mb: Monad[B]) -> Monad[B]:
        return self.flat_map(lambda _: mb)

    def map(self, func: Callable[[A], B]) -> Monad[B]:
        """m a -> (a -> b) -> m b"""
        def a_to_mb(some_a: A) -> Monad[B]:
            return compose(self.pure, func)(some_a)

        return self.flat_map(a_to_mb)
