from hypothesis import given, infer
import hypothesis.strategies as st
from typing import TypeVar

import pymonads.tests.functor_laws as fl
from pymonads import Either, Right, Left
from pymonads.either import pure
from pymonads.utils import identity, compose

A = TypeVar('A')
B = TypeVar('B')

def eithers():
    return st.one_of(st.builds(Right, st.integers()), st.builds(Left, st.integers()))

# Test that Either obeys the functor laws.
@given(either=eithers())
def test_either_preserves_identity_morhpisms(either):
    assert fl.functor_preserves_identity_morphisms(either)

@given(either=eithers())
def test_either_preserves_composition_of_morphisms(either):
    f = lambda x: x * 4
    g = lambda x: x / 2
    assert fl.functor_preserves_composition_of_morphisms(either, f, g)

# Test that Either obeys the applicative laws.
@given(either=eithers())
def test_applicative_identity_law(either):
    assert either.amap(pure(identity)) == either
