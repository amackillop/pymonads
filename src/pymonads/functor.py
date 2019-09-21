"""Functor base class"""

from __future__ import annotations

import abc
from functools import partial
from typing import Generic, TypeVar, Callable

from pymonads.utils import const, compose

T_co = TypeVar('T_co', covariant=True)

A = TypeVar('A')

class Functor(Generic[T_co], metaclass=abc.ABCMeta):
    """docstring"""

    @abc.abstractmethod
    def fmap(self, func: Callable[..., A]) -> Functor[A]:
        """fmap"""

    def map_replace(self, value: A) -> Functor[A]:
        """The <$ operator"""
        return compose(self.fmap, const)(value)
