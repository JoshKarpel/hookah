from typing import Literal

from hookah import render, use_reducer

CounterAction = Literal["inc", "dec", "reset"]


def counter(state: int, action: CounterAction) -> int:
    match action:
        case "inc":
            return state + 1
        case "dec":
            return state - 1
        case "reset":
            return 0


def test_counter() -> None:
    def _(action: CounterAction) -> int:
        count, dispatch = use_reducer(counter, 0)
        dispatch(action)
        return count  # previous value!

    assert render(_, "inc") == 0
    assert render(_, "dec") == 1
    assert render(_, "inc") == 0
    assert render(_, "inc") == 1
    assert render(_, "reset") == 2
    assert render(_, "dec") == 0
    assert render(_, "reset") == -1
