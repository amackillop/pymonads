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
class Left(Monad[A]):
    """Some representation of an error. Further computations will no longer happen."""
    value: A

    def pure(value: A) -> Left[A]:
        return Left(value)

    def fmap(self, func: Callable[..., B]) -> Left[A]:
        return self

    def amap(self, fab: Applicative[Callable[..., B]]) -> Left[A]:
        return self

    def flat_map(self, func: Callable[[A], Monad[A]]) -> Left[A]:
        return self


@dataclass(frozen=True, repr=False)
class Right(Monad[B]):
    """A successful result that will propagate."""
    value: B

    def pure(value: B) -> Right[B]:
        return Right(value)

    def fmap(self, func: Callable[..., A]) -> Right[A]:
        return Right(func(self.value))

    def amap(self, fab: Applicative[A]) -> Right[A]:
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[[B], Either[A, B]]) -> Either[A, B]:
        return func(self.value)

Either = Union[Left[A], Right[B]]
Me = Monad[Either[A, B]]

def pure(value: B) -> Right[B]:
    return Right(value)

def is_left(either: Either) -> bool:
    return isinstance(either, Left)

def is_right(either: Either) -> bool:
    return isinstance(either, Right)

@curry
def either(func_left: Callable[[A], C], func_right: Callable[[B], C], either: Union[Left, Right]) -> C:
    val = either.value
    return func_right(val) if is_right(either) else func_left(val)

def lefts(eithers: Iterable[Either]) -> Iterator[A]:
    return (either.value() for either in eithers if is_left(either))

def rights(eithers: Iterable[Either]) -> Iterator[B]:
    return (either.value() for either in eithers if is_right(either))
