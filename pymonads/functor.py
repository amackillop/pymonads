"""Functor base class"""

from __future__ import annotations
from dataclasses import dataclass

from functools import partial
from typing import Generic, TypeVar, Callable
from abc import ABC, abstractmethod, abstractproperty

from dataclasses import dataclass

from pymonads.utils import const, compose

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True, repr=False)
class DataClassMixin(Generic[A]):
    """A dataclass mixin.
    
    This is required to get around a mypy error.

    See: https://github.com/python/mypy/issues/5374#issuecomment-568335302
    """

    value: A

class Functor(DataClassMixin[A], ABC):
    """docstring"""

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    @abstractmethod
    def fmap(self, func: Callable[[A], B]) -> Functor[B]:
        """fmap"""

    def map_replace(self, value: B) -> Functor[B]:
        """The <$ operator"""
        return compose(self.fmap, const)(value)
