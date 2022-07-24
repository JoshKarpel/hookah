from hookah import run, use_ref


def test_ref_is_the_same_between_runs() -> None:
    def _() -> list[int]:
        return use_ref([1]).current

    a = run(_)
    assert a == [1]

    a.append(2)

    b = run(_)
    assert b == [1, 2]
    assert a is b
