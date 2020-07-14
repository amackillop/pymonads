from __future__ import annotations

from abc import ABC, ABCMeta
from dataclasses import dataclass
from pymonads.functor import Functor
from pymonads.applicative import Applicative
from pymonads.monad import Monad
from typing import TypeVar, Generic, Callable, Union, Any, Iterable, Iterator, Type

from numbers import Complex, Integral, Number

from pymonads.utils import curry


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

E = TypeVar("E")
T = TypeVar("T")

class _Either(Monad[A]):
    """"""

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    @classmethod
    def pure(cls, value):
        return Right(value)

    def is_left(self) -> bool:
        return isinstance(self, Left)

    def is_right(self) -> bool:
        return isinstance(self, Right)



class Left(_Either, Generic[A]):
    """"""

    def fmap(self, func: Callable[[A], B]) -> _Either[B]:
        """"""
        return self

    def amap(self, fab: Applicative[Callable[[A], B]]) -> _Either[B]:
        """"""
        return self

    def flat_map(self, func: Callable[[A], Monad[B]]) -> _Either[B]:
        """"""
        return self


class Right(_Either, Generic[A]):
    """"""

    def fmap(self, func: Callable[[A], B]) -> _Either[B]:
        """"""
        return Right(func(self.value))

    def amap(self, fab: Applicative[Callable[[A], B]]) -> _Either[B]:
        """"""
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[[A], _Either[B]]) -> _Either[B]:
        """"""
        return func(self.value)


Either = Union[Left[E], Right[T]]

@curry
def either(either_: Either, left_func: Callable[[E], C], right_func: Callable[[T], C]) -> C:
    val = either_.value
    return left_func(val) if either_.is_left() else right_func(val)

def lefts(eithers: Iterable[Either]) -> Iterator[E]:
    return (either.value for either in eithers if either.is_left())


def rights(eithers: Iterable[Either]) -> Iterator[T]:
    return (either.value for either in eithers if either.is_right())


ThrowsError = Either[str, T]

a: Either[str, int] = Left("sss")
b: Either[str, float] = Right(8)


# def division(num: int, div: int) -> Either[str, int]:
#     if div == 0:
#         return Left("Error!")

#     result = num / div
#     return Right(result)
