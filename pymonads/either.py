"""
The Either monad. Inspired by Haskell as a way to handle errors without having
to raise exceptions.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, replace
from typing import TypeVar, Generic, Callable, Union, Any, Iterable, Iterator, Type

from pymonads.monad import Monad
from pymonads.applicative import Applicative
from pymonads.utils import curry

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

E = TypeVar('E')
T = TypeVar('T')
U = TypeVar('U')

@dataclass(frozen=True, repr=False)
class _Either(Generic[T]):
    """Common code between Left and Right"""

    _value: T  

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    @property
    def value(self):
        return self._value

    @classmethod
    def pure(cls, value: T) -> Right[T]:
        return Right(value)

    def is_left(self) -> bool:
        return isinstance(self, Left)


    def is_right(self) -> bool:
        return isinstance(self, Right)

    @curry
    def either(self, left_func: Callable[[E], C], right_func: Callable[[T], C]) -> C:
        val = self.value
        return left_func(val) if self.is_left() else right_func(val)



class Left(_Either, Monad[E]):
    """Some representation of an error. Further computations will no longer happen."""

    def fmap(self, _: Callable[[E], U]) -> Left[E]:
        return self

    def amap(self, _: Applicative[Callable[[E], U]]) -> Left[E]:
        return self

    def flat_map(self, _: Callable[..., Monad[U]]) -> Left[E]:
        return self


class Right(_Either, Monad[T]):
    """A successful result that will propagate."""

    def fmap(self, func: Callable[[T], U]) -> Right[U]:
        return Right(func(self.value))

    def amap(self, fab: Applicative[Callable[[T], U]]) -> Right[U]:
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[[T], Either[U]]) -> Either[U]:
        return func(self.value)


Either = Monad[Union[Left[Any], Right[T]]]

def lefts(eithers: Iterable[Either]) -> Iterator[E]:
    return (either.value for either in eithers if either.is_left())


def rights(eithers: Iterable[Either]) -> Iterator[T]:
    return (either.value for either in eithers if either.is_right())
