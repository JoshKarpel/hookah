from __future__ import annotations

from collections.abc import Sequence
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Callable, Generic, ParamSpec, TypeVar

T = TypeVar("T")
A = TypeVar("A")
P = ParamSpec("P")

current_context: ContextVar[Context[Any, Any]] = ContextVar("current_context")


class Context(Generic[P, T]):
    def __init__(self, func: Callable[P, T]):
        self.func = func
        self.current_hook = 0
        self.hooks: dict[int, Any] = {}

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        current_context.set(self)
        self.current_hook = 0
        return self.func(*args, **kwargs)


def use_state(initial_value: T) -> tuple[T, Callable[[T], None]]:
    ctx = current_context.get()

    value: T = ctx.hooks.setdefault(ctx.current_hook, initial_value)

    i = ctx.current_hook  # capture value now for setter closure

    def setter(value: T) -> None:
        ctx.hooks[i] = value

    ctx.current_hook += 1

    return value, setter


def use_reducer(reducer: Callable[[T, A], T], initial_state: T) -> tuple[T, Callable[[A], None]]:
    ctx = current_context.get()

    reducer = ctx.hooks.setdefault(ctx.current_hook, reducer)

    state_idx = ctx.current_hook + 1
    state = ctx.hooks.setdefault(state_idx, initial_state)

    def dispatch(action: A) -> None:
        ctx.hooks[state_idx] = reducer(ctx.hooks[state_idx], action)

    ctx.current_hook += 2
    return state, dispatch


@dataclass
class Ref(Generic[T]):
    current: T


def use_ref(initial_value: T) -> Ref[T]:
    ctx = current_context.get()

    box: Ref[T] = ctx.hooks.setdefault(ctx.current_hook, Ref(initial_value))

    ctx.current_hook += 1

    return box


def use_effect(callback, deps: Sequence[object] | None = None) -> None:  # type: ignore[no-untyped-def]
    ctx = current_context.get()

    previous_deps = ctx.hooks.get(ctx.current_hook, [])
    if deps is None:
        callback()
    elif deps != previous_deps:
        callback()
        ctx.hooks[ctx.current_hook] = list(deps)

    ctx.current_hook += 1
