"""
The Either monad. Inspired by Haskell as a way to handle errors without having
to raise exceptions.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, replace
from typing import TypeVar, Generic, Callable, Union, Any

from monad import Monad
from applicative import Applicative

A = TypeVar('A')
B = TypeVar('B')

class Either(Monad, metaclass=abc.ABCMeta):
    """The either base class. Subtypes are either Left or Right."""

    @staticmethod
    def pure(value: A) -> Right[A]:
        return Right(value)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

@dataclass(frozen=True, repr=False)
class Left(Either, Generic[A]):
    """Some representation of an error. Further computations will no longer happen."""
    value: A

    def fmap(self, func: Callable[..., B]) -> Left[A]:
        return self

    def amap(self, fab: Applicative[Callable[..., B]]) -> Left[A]:
        return self

    def flat_map(self, func: Callable[..., Monad[B]]) -> Left[A]:
        return self


@dataclass(frozen=True, repr=False)
class Right(Either, Generic[B]):
    """A successful result that will propagate."""
    value: B

    def fmap(self, func: Callable[..., A]) -> Right[A]:
        return Right(func(self.value))

    def amap(self, fab: Applicative[Callable[..., A]]) -> Right[A]:
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[..., Either[A, B]]) -> Either[A, B]:
        return func(self.value)
