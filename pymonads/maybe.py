from __future__ import annotations

from pymonads.applicative import Applicative
from pymonads.monad import Monad
from pymonads.either import Either
from typing import List, TypeVar, Generic, Callable, Union, Iterable, Iterator, Type

from pymonads.utils import curry


from dataclasses import dataclass

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class _Maybe(Monad[A]):
    """"""

    @classmethod
    def pure(cls, value):
        return Just(value)

    def is_just(self) -> bool:
        return isinstance(self, Just)

    def is_nothing(self) -> bool:
        return isinstance(self, Nothing)


class Nothing(_Maybe):
    """"""

    def __init__(self):
        ...

    def __repr__(self):
        return "Nothing"

    @property
    def value(self):
        return None

    def fmap(self, func: Callable[[A], B]) -> _Maybe[B]:
        """"""
        return self

    def amap(self, fab: Applicative[Callable[[A], B]]) -> _Maybe[B]:
        """"""
        return self

    def flat_map(self, func: Callable[[A], Monad[B]]) -> _Maybe[B]:
        """"""
        return self


class Just(_Maybe[A]):
    """"""

    def fmap(self, func: Callable[[A], B]) -> _Maybe[B]:
        return Just(func(self.value))

    def amap(self, fab: Applicative[Callable[[A], B]]) -> _Maybe[B]:
        """"""
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[[A], _Maybe[B]]) -> _Maybe[B]:
        """"""
        return func(self.value)


Maybe = Union[Nothing, Just[A]]


def maybe(default: B, func: Callable[[A], B], maybe_: Maybe[A]) -> B:
    """The maybe function takes a default value, a function, and a Maybe value. 
    
    If the Maybe value is Nothing, the function returns the default value. 
    Otherwise, it applies the function to the value inside the Just and returns the result.
    """
    return func(maybe_.value) if maybe_.is_just() else default


def from_just(maybe_: Maybe[A]) -> A:
    """Extract the element out of a Just or throw an error if its Nothing."""
    if maybe_.is_nothing():
        raise RuntimeError("maybe.from_just called on Nothing")
    return maybe_.value


def from_maybe(default: A, maybe_: Maybe[A]) -> A:
    """The from_maybe function takes a default value and and Maybe value. 
    
    If the Maybe is Nothing, it returns the default value.
    Otherwise, it returns the value contained in the Maybe.
    """
    return maybe_.value if maybe_.is_just() else default


def list_to_maybe(elems: List[A]) -> Maybe[A]:
    """
    The list_to_maybe function returns Nothing on an empty list or 
    Just a where a is the first element of the list.
    """
    return Just(elems[0]) if elems else Nothing()


def maybe_to_list(maybe_: Maybe[A]) -> List[A]:
    """
    The maybeToList function returns an empty list when given Nothing 
    or a singleton list when given Just.
    """
    return [from_just(maybe_)] if maybe_.is_just() else []

def cat_maybes(maybes: Iterable[Maybe[A]]) -> Iterable[A]:
    return (from_just(maybe_) for maybe_ in maybes if maybe_.is_just())

def map_maybe(func: Callable[[A], Maybe[B]], elems: Iterable[A]) -> Iterable[B]:
    for elem in elems:
        val = func(elem)
        if val.is_just():
            yield from_just(val)