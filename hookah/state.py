from __future__ import annotations

from typing import Callable, Tuple, TypeVar, cast

T = TypeVar("T")
Setter = Callable[[T], None]


__current_hook = 0
__hooks: dict[int, object] = {}


def render(func):  # type: ignore[no-untyped-def]
    global __current_hook
    __current_hook = 0

    return func()


def incr(func):  # type: ignore[no-untyped-def]
    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        r = func(*args, **kwargs)
        global __current_hook
        __current_hook += 1
        # print(f"incr {__current_hook}")
        return r

    return wrapper


@incr
def use_state(initial_value: T) -> Tuple[T, Setter[T]]:
    # print(f"g pre  {__current_hook=} {__hooks=}")
    value = cast(T, __hooks.setdefault(__current_hook, initial_value))
    # print(f"g post {__current_hook=} {__hooks=} {value=}")

    i = __current_hook

    def setter(value: T) -> None:
        # print(f"s {i=} {value=} {__hooks=}")
        __hooks[i] = value

    return value, setter
