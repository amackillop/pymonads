from __future__ import annotations

import abc
from dataclasses import dataclass, replace
from typing import TypeVar, Generic, Callable, Union, Any

A = TypeVar('A')
B = TypeVar('B')
T = TypeVar('T')
E = TypeVar('E')

from monad import Monad
from applicative import Applicative

class Either(Monad, Generic[E, T], metaclass=abc.ABCMeta):
    """Etiher Monad"""

    @staticmethod
    def pure(value: A) -> Right[A]:
        return Right(value)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

@dataclass(frozen=True, repr=False)
class Left(Either, Generic[A]):
    """"""
    value: A

    def fmap(self, func: Callable[..., B]) -> Left[A]:
        return self

    def amap(self, fab: Applicative[Callable[..., B]]) -> Left[A]:
        return self

    def flat_map(self, func: Callable[..., Monad[B]]) -> Left[A]:
        return self


@dataclass(frozen=True, repr=False)
class Right(Either, Generic[B]):
    """"""
    value: B

    def fmap(self, func: Callable[..., A]) -> Right[A]:
        return Right(func(self.value))

    def amap(self, fab: Applicative[Callable[..., A]]) -> Right[A]:
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[..., Either[A, B]]) -> Either[A, B]:
        return func(self.value)
