from pytest_mock import MockerFixture

from hookah import Context, use_effect


def test_callback_is_called_every_time_if_no_deps(mocker: MockerFixture) -> None:
    mock = mocker.Mock()

    @Context
    def _() -> None:
        use_effect(mock)

    _()
    assert mock.call_count == 1

    _()
    assert mock.call_count == 2

    _()
    assert mock.call_count == 3


def test_callback_is_called_based_on_whether_dependencies_changed(mocker: MockerFixture) -> None:
    mock = mocker.Mock()
    deps = [0]  # you wouldn't normally mutate it like this...

    @Context
    def _() -> None:
        use_effect(mock, deps)

    _()
    assert mock.call_count == 1

    _()
    assert mock.call_count == 1

    deps[0] = 1

    _()
    assert mock.call_count == 2

    _()
    assert mock.call_count == 2

    deps[0] = 0

    _()
    assert mock.call_count == 3

    _()
    assert mock.call_count == 3
