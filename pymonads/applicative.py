"""Functor base class"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Any

from pymonads.functor import Functor
from pymonads.utils import identity, curry, compose, const, flip

T_co = TypeVar('T_co', covariant=True)

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')

Func = TypeVar('Func', bound=Callable[..., Any])

# @dataclass(frozen=True)
class Applicative(Functor, Generic[T_co], metaclass=abc.ABCMeta):
    """An applicative functor"""
    
    @property
    @abc.abstractmethod
    def value(self) -> Any:
        """Some value within the Applicative"""

    @abc.abstractmethod
    def pure(self, value: A) -> Applicative[A]:
        """"""

    @abc.abstractmethod
    def amap(self, fab: Applicative[Callable[..., B]]) -> Applicative[B]:
        """<*>"""

    def sequence_right(self, fb: Applicative[B]) -> Applicative[B]:
        return lift_a_2(flip(const))

    def sequence_left(self, fb: Applicative[B]) -> Applicative[A]:
        return lift_a_2(const)

Ap = Applicative

@curry
def lift_a_1(func: Callable[[A], B], fa: Ap[A]) -> Ap[B]:
    return compose(fa.amap, Applicative.pure)(func)

@curry
def lift_a_2(func: Callable[[A, B], C], fa: Ap[A], fb: Ap[B]) -> Ap[C]:
    """liftA2"""
    return compose(fb.amap, fa.fmap)(func)

@curry
def lift_a_3(func: Callable[[A, B, C], D], fa: Ap[A], fb: Ap[B], fc: Ap[C]) -> Ap[D]:
    return fc.amap(lift_a_2(func, fa, fb))
