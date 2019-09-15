"""Functor base class"""

from __future__ import annotations

import abc
from functools import partial
from typing import Generic, TypeVar, Callable, Any

from functor import Functor
from utils import identity, curry, compose

T_co = TypeVar('T_co', covariant=True)

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

class Applicative(Functor, Generic[T_co], metaclass=abc.ABCMeta):
    """An applicative functor"""

    @classmethod
    @abc.abstractmethod
    def pure(cls, value: A) -> Applicative[A]:
        """"""

    @abc.abstractmethod
    def amap(self, fa: Applicative[A]) -> Applicative[B]:
        """<*>"""

    def fmap(self: Applicative[A], func: Callable[..., B]) -> Applicative[B]:
        return self.amap(Applicative.pure(func))

@curry
def lift_a_2(func: Callable[[A, B], C], fa: Applicative[A], fb: Applicative[B]) -> Applicative[C]:
    """liftA2"""
    return compose(fb.amap, fa.fmap)(func)


