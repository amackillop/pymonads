from hypothesis import given, infer
import hypothesis.strategies as st
from typing import TypeVar, Union

from either import Either, Right, Left
from utils import identity, compose

A = TypeVar('A')
B = TypeVar('B')

def eithers():
    return st.one_of(st.builds(Right, st.integers()), st.builds(Left, st.integers()))

def functions():
    return st.one_of()
# Test that Either obeys the functor laws.
@given(either=eithers())
def test_either_fmap_id_equals_id_either(either):
    assert either.fmap(identity) == identity(either)

@given(either=eithers(), f=lambda x: x * 4, g=lambda x: x / 2)
def test_fmap_a_compose_b_equals_fmap_a_compose_fmap_b(either, f, g):
    
    
    assert either.fmap(compose(f, g)) == either.fmap(g).fmap(f)

# Test that Either obeys the applicative laws.
@given(either=eithers())
def test_applicative_identity_law(either):
    assert either.amap(Either.pure(identity)) == either

# @given(either=eithers())
# def test_applicative_homomorphism_law(either):

#     Either.pure()
    