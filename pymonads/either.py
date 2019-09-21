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


@dataclass(frozen=True)
class Left(Monad[E]):
    """Some representation of an error. Further computations will no longer happen."""
    value: E

    def pure(self, value: A) -> Left[A]:
        return Left(value)

    def fmap(self, func: Callable[..., B]) -> Left[E]:
        return self

    def amap(self, fab: Applicative[Callable[..., B]]) -> Left[E]:
        return self

    def flat_map(self, func: Callable[..., Monad[B]]) -> Left[E]:
        return self


@dataclass(frozen=True, repr=False)
class Right(Monad[T]):
    """A successful result that will propagate."""
    value: T

    def pure(self, value: A) -> Right[A]:
        return Right(value)

    def fmap(self, func: Callable[[T], B]) -> Right[B]:
        return Right(func(self.value))

    def amap(self, fab: Applicative[Callable[[T], B]]) -> Right[B]:
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[[T], Either[E, B]]) -> Either[E, B]:
        return func(self.value)

Either = Union[Left[E], Right[T]]

def pure(value: T) -> Right[T]:
    return Right(value)

def is_left(either: Either[E, A]) -> bool:
    return isinstance(either, Left)

def is_right(either: Either[E, A]) -> bool:
    return isinstance(either, Right)

@curry
def either(func_left: Callable[[E], C], func_right: Callable[[T], C], either: Either) -> C:
    val = either.value
    return func_right(val) if is_right(either) else func_left(val)

def lefts(eithers: Iterable[Either]) -> Iterator[A]:
    return (either.value for either in eithers if is_left(either))

def rights(eithers: Iterable[Either]) -> Iterator[B]:
    return (either.value for either in eithers if is_right(either))
