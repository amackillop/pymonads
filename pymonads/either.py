from __future__ import annotations

from typing import Tuple, TypeVar, Generic, Callable, Union, Iterable, Iterator
from pymonads.applicative import Applicative
from pymonads.monad import Monad
from pymonads.utils import curry, partition


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class _Either(Monad[A]):
    """"""

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


Either = Union[Left[A], Right[B]]


@curry
def either(
    left_func: Callable[[A], C], right_func: Callable[[B], C], either_: Either
) -> C:
    val = either_.value
    return left_func(val) if either_.is_left() else right_func(val)


def lefts(eithers: Iterable[Either]) -> Iterator[A]:
    return (either.value for either in eithers if either.is_left())


def rights(eithers: Iterable[Either]) -> Iterator[B]:
    return (either.value for either in eithers if either.is_right())


def from_left(default: A, either_: Either[A, B]) -> A:
    """Return the contents of a Right-value or a default value otherwise."""
    return either_.value if either_.is_left() else default


def from_right(default: B, either_: Either[A, B]) -> B:
    """Return the contents of a Right-value or a default value otherwise."""
    return either_.value if either_.is_right() else default


def partition_eithers(eithers: Iterable[Either]) -> Tuple[Iterable[A], Iterable[B]]:
    return partition(lambda x: x.is_right(), eithers)

