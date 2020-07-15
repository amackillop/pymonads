from typing import TypeVar
from hypothesis import given
import hypothesis.strategies as st

import tests.functor_laws as fl
import tests.applicative_laws as al
import tests.monad_laws as ml

from pymonads.maybe import Just, Nothing

A = TypeVar("A")
B = TypeVar("B")


def maybes() -> st.SearchStrategy:
    return st.one_of(st.builds(Just, st.integers()), st.builds(Nothing))


def maybes_applicative() -> st.SearchStrategy:
    f = st.just(lambda x: x * 4)
    return st.builds(Just, f)


# Test that Either obeys the functor laws.
@given(maybe=maybes())
def test_maybe_preserves_identity_morhpisms(maybe):
    assert fl.functor_preserves_identity_morphisms(maybe)


@given(maybe=maybes())
def test_maybe_preserves_composition_of_morphisms(maybe):
    f = lambda x: x * 4
    g = lambda x: x / 2
    assert fl.functor_preserves_composition_of_morphisms(maybe, f, g)


# Test that maybe obeys the applicative laws.
@given(maybe=maybes())
def test_maybe_obeys_identity_law(maybe):
    assert al.applicative_preserves_identity_morphism(maybe)


@given(x=st.integers())
def test_maybe_is_homomorphic(x):
    f = lambda a: a * 4
    assert al.applicative_preserves_function_application(Just, f, x)


@given(maybe=maybes_applicative(), x=st.integers())
def test_maybe_obeys_interchangeability(maybe, x):
    assert al.applicative_is_interchangeable(maybe, x)


# Test that maybe obeys the Monad laws.
@given(maybe=maybes(), x=st.integers())
def test_maybe_obeys_left_identity(maybe, x):
    f = lambda a: a * 4
    assert ml.monad_respects_left_identity(maybe, x, f)


@given(maybe=maybes(), x=st.integers())
def test_maybe_obeys_Just_identity(maybe, x):
    f = lambda a: a * 4
    assert ml.monad_respects_right_identity(maybe, x, f)


@given(maybe=maybes())
def test_maybe_associativity(maybe):
    f = lambda a: Just(a * 4)
    g = lambda b: Just(b / 2)
    assert ml.monad_respects_associativity(maybe, f, g)


# Some other basic tests
