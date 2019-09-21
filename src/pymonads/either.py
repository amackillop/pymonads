"""
The Either monad. Inspired by Haskell as a way to handle errors without having
to raise exceptions.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, replace
from typing import TypeVar, Generic, Callable, Union, Any, Iterable, Iterator

from pymonads.monad import Monad
from pymonads.applicative import Applicative
from pymonads.utils import curry

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

E = TypeVar('E')
T = TypeVar('T')

class Either(Monad, Generic[E, T], metaclass=abc.ABCMeta):
    """The Either base class. Subtypes are either Left or Right."""

    @staticmethod
    def pure(value: A) -> Right[A]:
        return Right(value)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'


@dataclass(frozen=True, repr=False)
class Left(Either, Generic[E]):
    """Some representation of an error. Further computations will no longer happen."""
    value: E

    def fmap(self, func: Callable[..., B]) -> Left[E]:
        return self

    def amap(self, fab: Applicative[Callable[..., B]]) -> Left[E]:
        return self

    def flat_map(self, func: Callable[..., Monad[B]]) -> Left[E]:
        return self


@dataclass(frozen=True, repr=False)
class Right(Either, Generic[T]):
    """A successful result that will propagate."""
    value: T

    def fmap(self, func: Callable[..., A]) -> Right[A]:
        return Right(func(self.value))

    def amap(self, fab: Applicative[Callable[..., A]]) -> Right[A]:
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[..., Either[A, B]]) -> Either[A, B]:
        return func(self.value)


def is_left(either: Either[A, B]) -> bool:
    return isinstance(either, Left)

def is_right(either: Either[A, B]) -> bool:
    return isinstance(either, Right)

@curry
def either(func_left: Callable[[A], C], func_right: Callable[[B], C], either: Either[A, B]) -> C:
    val = either.value
    return func_right(val) if is_right(either) else func_left(val)

def lefts(eithers: Iterable[Either[A, B]]) -> Iterator[A]:
    return (either.value for either in eithers if is_left(either))

def rights(eithers: Iterable[Either[A, B]]) -> Iterator[A]:
    return (either.value for either in eithers if is_right(either))
