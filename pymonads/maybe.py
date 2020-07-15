from __future__ import annotations

from pymonads.applicative import Applicative
from pymonads.monad import Monad
from pymonads.either import Either
from typing import TypeVar, Generic, Callable, Union, Iterable, Iterator, Type

from pymonads.utils import curry


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

E = TypeVar("E")
T = TypeVar("T")


class Maybe(Monad[A]):
    """"""

    @classmethod
    def pure(cls, value):
        return Just(value)


class Nothing(Maybe):
    """"""

    def __init__(self):
        ...

    def __repr__(self):
        return "Nothing"

    @property
    def value(self):
        return None

    def fmap(self, func: Callable[[A], B]) -> Maybe[B]:
        """"""
        return self

    def amap(self, fab: Applicative[Callable[[A], B]]) -> Maybe[B]:
        """"""
        return self

    def flat_map(self, func: Callable[[A], Monad[B]]) -> Maybe[B]:
        """"""
        return self


class Just(Maybe):
    """"""

    def fmap(self, func: Callable[[A], B]) -> Maybe[B]:
        return Just(func(self.value))

    def amap(self, fab: Applicative[Callable[[A], B]]) -> Maybe[B]:
        """"""
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[[A], Maybe[B]]) -> Maybe[B]:
        """"""
        return func(self.value)
