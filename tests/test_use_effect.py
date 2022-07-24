from pytest_mock import MockerFixture

from hookah import render, use_effect


def test_callback_is_called_every_time_if_no_deps(mocker: MockerFixture) -> None:
    mock = mocker.Mock()

    def _() -> None:
        use_effect(mock)

    render(mock)
    assert mock.call_count == 1

    render(mock)
    assert mock.call_count == 2

    render(mock)
    assert mock.call_count == 3


def test_callback_is_called_based_on_whether_dependencies_changed(mocker: MockerFixture) -> None:
    mock = mocker.Mock()
    deps = [0]  # you wouldn't normally mutate it like this...

    def _() -> None:
        use_effect(mock, deps)

    render(_)
    assert mock.call_count == 1

    render(_)
    assert mock.call_count == 1

    deps[0] = 1

    render(_)
    assert mock.call_count == 2

    render(_)
    assert mock.call_count == 2

    deps[0] = 0

    render(_)
    assert mock.call_count == 3

    render(_)
    assert mock.call_count == 3
