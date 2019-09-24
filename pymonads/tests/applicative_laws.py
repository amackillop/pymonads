"""
The Applicative Functor Laws.
"""

from typing import TypeVar, Callable, Type

from pymonads.applicative import Applicative 
from pymonads.utils import identity, compose, apply

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

Ap = Applicative

def applicative_preserves_identity_morphism(applicative: Ap) -> bool:
    return applicative.amap(applicative.__class__.pure(identity)) == applicative

def applicative_preserves_function_application(ap_class: Type[Ap], f: Callable[[A], B], x: A) -> bool:
    pure = ap_class.pure
    return pure(x).amap(pure(f)) == pure(f(x))

def applicative_is_interchangeable(ap_class: Type[Ap], applicative: Ap, x: A) -> bool:
    pure = ap_class.pure
    return pure(x).amap(applicative) == applicative.amap(pure(lambda func: func(x)))

def applicative_preserves_composition(ap_class: Type[Ap], ap_a: Ap, ap_b: Ap, ap_c: Ap) -> bool:
    pure = ap_class.pure
    return ap_c.amap(ap_b.amap(ap_a.amap(pure(compose)))) == ap_c.amap(ap_b).amap(ap_c)
