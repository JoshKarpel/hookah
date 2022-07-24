from hookah import run, use_state


def counter(inc: int = 1) -> int:
    x, set_x = use_state(0)

    set_x(x + inc)

    return x


def two_counters() -> tuple[int, int]:
    return counter(inc=1), counter(inc=-1)


def test_setter_affects_subsequent_returns() -> None:
    assert run(counter) == 0
    assert run(counter) == 1
    assert run(counter) == 2


def test_states_are_isolated_from_each_other() -> None:
    assert run(two_counters) == (0, 0)
    assert run(two_counters) == (1, -1)
    assert run(two_counters) == (2, -2)
