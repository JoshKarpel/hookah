from pytest_mock import MockerFixture

from hookah import run, use_effect


def test_callback_is_called_every_time_if_no_deps(mocker: MockerFixture) -> None:
    mock = mocker.Mock()

    def _() -> None:
        use_effect(mock)

    run(mock)
    assert mock.call_count == 1

    run(mock)
    assert mock.call_count == 2

    run(mock)
    assert mock.call_count == 3


def test_callback_is_called_based_on_whether_dependencies_changed(mocker: MockerFixture) -> None:
    mock = mocker.Mock()
    deps = [0]  # you wouldn't normally mutate it like this...

    def _() -> None:
        use_effect(mock, deps)

    run(_)
    assert mock.call_count == 1

    run(_)
    assert mock.call_count == 1

    deps[0] = 1

    run(_)
    assert mock.call_count == 2

    run(_)
    assert mock.call_count == 2

    deps[0] = 0

    run(_)
    assert mock.call_count == 3

    run(_)
    assert mock.call_count == 3
