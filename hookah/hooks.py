from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Callable, TypeVar

T = TypeVar("T")
A = TypeVar("A")

__current_hook = 0
__hooks: dict[int, Any] = {}


def render(func, *args, **kwargs):  # type: ignore[no-untyped-def]
    global __current_hook
    __current_hook = 0

    return func(*args, **kwargs)


def use_state(initial_value: T) -> tuple[T, Callable[[T], None]]:
    global __current_hook
    value: T = __hooks.setdefault(__current_hook, initial_value)

    i = __current_hook

    def setter(value: T) -> None:
        __hooks[i] = value

    __current_hook += 1

    return value, setter


def use_effect(callback, deps: Sequence[object] | None = None) -> None:  # type: ignore[no-untyped-def]
    global __current_hook

    previous_deps = __hooks.get(__current_hook, [])
    if deps is None:
        callback()
    elif deps != previous_deps:
        callback()
        __hooks[__current_hook] = list(deps)

    __current_hook += 1


def use_reducer(reducer: Callable[[T, A], T], initial_state: T) -> tuple[T, Callable[[A], None]]:
    global __current_hook

    reducer = __hooks.setdefault(__current_hook, reducer)

    state_idx = __current_hook + 1
    state = __hooks.setdefault(state_idx, initial_state)

    def dispatch(action: A) -> None:
        __hooks[state_idx] = reducer(__hooks[state_idx], action)

    __current_hook += 2
    return state, dispatch
