from __future__ import annotations

import abc
from dataclasses import dataclass, replace
from typing import TypeVar, Generic, Callable, Union, Any

A = TypeVar('A')
B = TypeVar('B')
T = TypeVar('T')
E = TypeVar('E')

from monad import Monad
from applicative import Applicative

class Either(Monad[Union[E,T]], Generic[E, T], metaclass=abc.ABCMeta):
    """Etiher Monad"""

    @property
    @abc.abstractmethod
    def value(self):
        """The wrapped value"""

    @classmethod
    def pure(cls, value: A):
        return Right(value)

    def fmap(self, func: Callable[..., B]) -> Either[A, B]:
        return Right(func(self.value)) if isinstance(self, Right) else self

    def amap(self, fab: Applicative[Callable[..., B]]) -> Either[A, B]:
        return self.fmap(fab.value)

    def flat_map(self, func: Callable[..., Either[A, B]]) -> Either[A, B]:
        return func(self.value) if isinstance(self, Right) else self

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

@dataclass(frozen=True, repr=False)
class Left(Either, Generic[A]):
    """"""
    value: A

@dataclass(frozen=True, repr=False)
class Right(Either, Generic[B]):
    """"""
    value: B

# @dataclass(frozen=True, repr=False)
# class Right(Either, Generic[T]):
#     """"""
#     value: T

#     def fmap(self, func: Callable[..., B]) -> Right[B]:
#         return Right(func(self.value))

#     def amap(self, fab: Applicative[Callable[[A, B], B]]) -> Right[B]:
#         return self.fmap(fab)

#     def flat_map(self, func: Callable[..., Either[E, T]]) -> Either[E, T]:
#         return func(self.value) 


