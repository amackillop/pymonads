"""Functor base class"""

from __future__ import annotations
from dataclasses import dataclass

from functools import partial
from typing import Generic, TypeVar, Callable
from abc import ABC, abstractmethod, abstractproperty

from dataclasses import dataclass

from pymonads.utils import const, compose

A_co = TypeVar("A_co", covariant=True)
T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True, repr=False)
class DataClassMixin(Generic[A_co]):
    """A dataclass mixin.
    
    This is required to get around a mypy error.

    See: https://github.com/python/mypy/issues/5374#issuecomment-568335302
    """

    value: A_co


class Functor(DataClassMixin, Generic[A_co], ABC):
    """docstring"""

    # @abstractproperty
    # def value(self) -> A_co:
    #     """Some value within the Functor"""

    @abstractmethod
    def fmap(self, func: Callable[[A_co], B]) -> Functor[B]:
        """fmap"""

    def map_replace(self, value: B) -> Functor[B]:
        """The <$ operator"""
        return compose(self.fmap, const)(value)
