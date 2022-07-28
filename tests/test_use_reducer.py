from typing import Literal

from hookah import Context, use_reducer

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
    @Context
    def _(action: CounterAction) -> int:
        count, dispatch = use_reducer(counter, 0)
        dispatch(action)
        return count  # previous value!

    assert _("inc") == 0
    assert _("dec") == 1
    assert _("inc") == 0
    assert _("inc") == 1
    assert _("reset") == 2
    assert _("dec") == 0
    assert _("reset") == -1
