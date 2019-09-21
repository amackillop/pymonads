import functools
from typing import TypeVar, Callable, Any

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

Func = TypeVar('Func', bound=Callable[..., Any])

def curry(func: Func):
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

def apply(func: Func, *args, **kwargs) -> Any:
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
