"""
The Applicative Functor Laws.
"""

from typing import TypeVar, Callable, Type

from pymonads.applicative import Applicative, pure 
from pymonads.utils import identity, compose

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

Ap = Applicative

def applicative_preserves_identity_morphism(ap: Ap) -> bool:
    return ap.amap(pure(ap.__class__, identity)) == ap

def applicative_preserves_function_application(ap_class: Type[Ap], f: Callable[[A], B], x: A) -> bool:
    return pure(ap_class, x).amap(pure(ap_class, f)) == pure(ap_class, f(x))

def applicative_is_interchangeable(ap: Ap, x: A) -> bool:
    return pure(ap.__class__, x).amap(ap) == ap.amap(pure(ap.__class__, lambda func: func(x)))

def applicative_preserves_composition(ap_a: Ap, ap_b: Ap, ap_c: Ap) -> bool:
    return ap_c.amap(ap_b.amap(ap_a.amap(pure(ap_a.__class__, compose)))) == ap_c.amap(ap_b).amap(ap_c)
