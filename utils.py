import functools
from typing import TypeVar, Callable, Any

A = TypeVar('A')
Func = TypeVar('Func', bound=Callable[..., Any])

def identity(value: A) -> A:
    """The identity function"""
    return value

def const(value: A, _) -> A:
    """ Simply returns it's first argument"""
    return value

def curry(func: Func):
    @functools.wraps(func)
    def curried(*args, **kwargs):
        if func.__code__.co_argcount <= len(args):
            return func(*args, **kwargs)
        return functools.partial(func, *args, **kwargs)
    return curried
