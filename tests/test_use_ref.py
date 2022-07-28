from hookah import Context, use_ref


def test_ref_is_the_same_between_runs() -> None:
    @Context
    def _() -> list[int]:
        return use_ref([1]).current

    a = _()
    assert a == [1]

    a.append(2)

    b = _()
    assert b == [1, 2]
    assert a is b
