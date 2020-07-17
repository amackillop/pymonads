import functools
import itertools as it
from typing import Iterable, Tuple, TypeVar, Callable, Any

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

Func = TypeVar("Func", bound=Callable[..., Any])


def curry(func: Func) -> Callable[..., Any]:
    """Apply automatic currying to a python function"""

    @functools.wraps(func)
    def curried(*args, **kwargs):
        if func.__code__.co_argcount <= len(args):
            return func(*args, **kwargs)
        return functools.partial(func, *args, **kwargs)

    return curried


def identity(value: A) -> A:
    """The identity function"""
    return value


def apply(func: Func, *args, **kwargs) -> A:
    return func(*args, **kwargs)


@curry
def const(value: A, _) -> A:
    """ Simply returns it's first argument"""
    return value


@curry
def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    return lambda x: f(g(x))


@curry
def flip(func: Callable[..., C], a: A, b: B) -> C:
    return func(b, a)


@curry
def partition(
    pred: Callable[[A], bool], iterable: Iterable[A]
) -> Tuple[Iterable[A], Iterable[A]]:
    """Use a predicate to partition entries into false entries and true entries
    
    partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    
    """
    t1, t2 = it.tee(iterable)
    return it.filterfalse(pred, t1), filter(pred, t2)
