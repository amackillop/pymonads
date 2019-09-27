from hypothesis import given, infer
import hypothesis.strategies as st
from typing import TypeVar

import pymonads.tests.functor_laws as fl
import pymonads.tests.applicative_laws as al
from pymonads import Either, Right, Left
from pymonads.either import pure, _Either
from pymonads.utils import identity, compose

A = TypeVar('A')
B = TypeVar('B')

def eithers() -> st.SearchStrategy:
    return st.one_of(st.builds(Right, st.integers()), st.builds(Left, st.integers()))

def eithers_applicative() -> st.SearchStrategy:
    f = st.just(lambda x: x*4)
    return st.builds(Right, f)

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
def test_either_obeys_identity_law(either):
    assert al.applicative_preserves_identity_morphism(either)

@given(x=st.integers())
def test_either_is_homomorphic(x):
    f = lambda a: a * 4
    assert al.applicative_preserves_function_application(_Either, f, x)

@given(either=eithers_applicative(), x=st.integers())
def test_either_obeys_interchangeability(either, x):
    assert al.applicative_is_interchangeable(_Either, either, x)

# Test that Either obeys the Monad laws.