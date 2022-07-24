# hookah

[![PyPI](https://img.shields.io/pypi/v/hookah)](https://pypi.org/project/hookah/)
[![Documentation Status](https://readthedocs.org/projects/hookah/badge/?version=latest)](https://hookah.readthedocs.io/en/latest/?badge=latest)
[![PyPI - License](https://img.shields.io/pypi/l/hookah)](https://pypi.org/project/hookah/)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/JoshKarpel/hookah/main.svg)](https://results.pre-commit.ci/latest/github/JoshKarpel/hookah/main)
[![codecov](https://codecov.io/gh/JoshKarpel/hookah/branch/main/graph/badge.svg?token=2sjP4V0AfY)](https://codecov.io/gh/JoshKarpel/hookah)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![GitHub issues](https://img.shields.io/github/issues/JoshKarpel/hookah)](https://github.com/JoshKarpel/hookah/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/JoshKarpel/hookah)](https://github.com/JoshKarpel/hookah/pulls)

hookah is a framework for building and presenting richly-styled presentations in your terminal using Python.

To see what hookah can do without installing it, you can view the demonstration deck in a container:
```bash
$ docker run -it --rm ghcr.io/joshkarpel/hookah
```
Alternatively, install hookah (`pip install hookah`) and run this command to view the demonstration deck:
```bash
$ hookah demo present
```

## Sandboxed Execution via Containers

hookah presentations are live Python code: they can do anything that Python can do.
You may want to run untrusted presentations (or even your own presentations) inside a container (but remember, even containers are not perfectly safe!).
We produce a [container image](https://github.com/users/JoshKarpel/packages/container/package/hookah)
that can be run by (for example) Docker.

Presentations without extra Python dependencies might just need to be bind-mounted into the container.
For example, if your demo file is at `$PWD/presentation/deck.py`, you could do
```bash
$ docker run -it --rm --mount type=bind,source=$PWD/presentation,target=/presentation ghcr.io/joshkarpel/hookah hookah present /presentation/deck.py
```

If the presentation has extra dependencies (like other Python packages),
we recommend building a new image that inherits our image (e.g., `FROM ghcr.io/joshkarpel/hookah:vX.Y.Z`).
hookah's image itself inherits from the [Python base image](https://hub.docker.com/_/python).

## Supported Systems

hookah currently relies on underlying terminal mechanisms that are only available on POSIX systems (e.g., Linux and MacOS).
If you're on Windows, you can use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) to run hookah.
