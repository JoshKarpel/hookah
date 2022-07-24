from hookah.state import render, use_state


def counter(inc: int = 1) -> int:
    x, set_x = use_state(0)

    set_x(x + inc)

    return x


def two_counters() -> tuple[int, int]:
    return counter(inc=1), counter(inc=-1)


def test_setter_affects_subsequent_returns() -> None:
    assert render(counter) == 0
    assert render(counter) == 1
    assert render(counter) == 2


def test_states_are_isolated_from_each_other() -> None:
    assert render(two_counters) == (0, 0)
    assert render(two_counters) == (1, -1)
    assert render(two_counters) == (2, -2)
