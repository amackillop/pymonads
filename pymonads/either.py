from __future__ import annotations

from abc import ABC, ABCMeta
from dataclasses import dataclass
from pymonads.functor import Functor
from pymonads.applicative import Applicative
from pymonads.monad import Monad
from typing import TypeVar, Generic, Callable, Union, Any, Iterable, Iterator, Type

from numbers import Complex, Integral, Number

from pymonads.utils import apply


A = TypeVar("A")
B = TypeVar("B")

E = TypeVar("E")
T_co = TypeVar("T_co", covariant=True)


class _Either(Monad[T_co]):
    """"""

    @classmethod
    def pure(cls, value):
        return Right(value)


class Left(_Either, Generic[E]):
    """"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def fmap(self, func: Callable[[A], B]) -> _Either[B]:
        """"""
        return self

    def amap(self, fab: Applicative[Callable[[A], B]]) -> _Either[B]:
        """"""
        return self

    def flat_map(self, func: Callable[[A], Monad[B]]) -> _Either[B]:
        """"""
        return self


class Right(_Either, Generic[T_co]):
    """"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def fmap(self, func: Callable[[T_co], B]) -> _Either[B]:
        """"""
        return Right(func(self.value))

    def amap(self, fab: Applicative[Callable[[T_co], B]]) -> _Either[B]:
        """"""
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[[A], Monad[B]]) -> _Either[B]:
        """"""
        return self


# Either = Union[Left[E], Right[T_co]]

# ThrowsError = Either[str, T]

# a: Either[str, int] = Left("sss")
# b: Either[str, float] = Right(8.)

# def division(num: int, div: int) -> ThrowsError[float]:
#     if div == 0:
#         return Left("Error!")

#     return Right(int(num/div))
