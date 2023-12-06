
# autorefine [![Package version](https://img.shields.io/pypi/v/autorefine?label=PyPI)](https://pypi.org/project/autorefine/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/autorefine.svg?logo=python&label=Python)](https://pypi.org/project/autorefine/)
[![Tests](https://github.com/bswck/autorefine/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/autorefine/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/autorefine.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/autorefine)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?label=Code%20style)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/bswck/autorefine.svg?label=License)](https://github.com/bswck/autorefine/blob/HEAD/LICENSE)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Standardize the refactoring process.

The project is aimed to provide a framework for the entire process of refactoring Python projects
from the very beginning to the very end:
- analyze the project with linters and type checkers,
- create a refactoring roadmap (like https://github.com/CERT-Polska/malduck/issues/110, but with more details available as a specialized document),
- create a delivery plan (like in the issue above),
- apply automatic fixes and commit them in reviewable chunks with meaningful descriptions,
- leave the rest for manual work,
- create a PR (like https://github.com/CERT-Polska/malduck/issues/111).

Created to accomplish https://github.com/jaraco/skeleton/issues/98 and personal use to raise awareness of best practices across the global Python community.

# Planned tooling
The project is planned to be a wrapper around the following well-tested & recognized tools:
- [MonkeyType](https://github.com/Instagram/MonkeyType#readme) for automatic type annotations generation,
- [Fixit](https://github.com/Instagram/Fixit#readme) for automatic fixes that require static analysis and scope analysis and planning of manual refactoring steps,
- [Ruff](https://github.com/astral-sh/ruff#readme) for automatic fixes and planning of manual refactoring steps,
- [pyupgrade](https://github.com/asottile/pyupgrade#readme) for automatic fixes,
- Static type checking:
  - [mypy](https://github.com/python/mypy#readme),
  - [pyre](https://github.com/facebook/pyre-check#readme),
  - [pytype](https://github.com/google/pytype#readme),
- [diff-cover](https://github.com/Bachmann1234/diff_cover#readme) for [coverage](https://github.com/nedbat/coverage#readme) reports on fixes,
- [smokeshow](https://github.com/samuelcolvin/smokeshow#readme) for hosting detailed refactoring roadmaps and delivery plans,
- [pandas](https://github.com/pandas-dev/pandas) for collecting tasks and creating markdown tables,
- [GitHub CLI](https://cli.github.com/) for creating tickets.

# Refactoring workflow
1. First off, check for type annotations and add them if missing using MonkeyType.

1. Analyze the project and create a refactoring roadmap.

   1. Check for type errors using static type checkers.

   1. Check for code style issues using linters.

1. Apply automatic fixes and commit them in reviewable chunks with meaningful descriptions.

1. Leave the rest for manual work.

1. Create a PR.

# Get inspired
- https://instagram-engineering.com/static-analysis-at-scale-an-instagram-story-8f498ab71a0c

# Installation
If you want to…



## …use this tool in your project 💻
You might simply install it with pip:

```shell
pip install autorefine
```

If you use [Poetry](https://python-poetry.org/), then run:

```shell
poetry add autorefine
```

## …contribute to [autorefine](https://github.com/bswck/autorefine) 🚀


> [!Note]
> If you use Windows, it is highly recommended to complete the installation in the way presented below through [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).



1.  Fork the [autorefine repository](https://github.com/bswck/autorefine) on GitHub.

1.  [Install Poetry](https://python-poetry.org/docs/#installation).<br/>
    Poetry is an amazing tool for managing dependencies & virtual environments, building packages and publishing them.
    You might use [pipx](https://github.com/pypa/pipx#readme) to install it globally (recommended):

    ```shell
    pipx install poetry
    ```

    <sub>If you encounter any problems, refer to [the official documentation](https://python-poetry.org/docs/#installation) for the most up-to-date installation instructions.</sub>

    If you want to use pipx to install dev dependencies as well, install the [poetry apps](https://github.com/bswck/poetry-apps#readme) plugin:
    ```shell
    pipx inject poetry poetry-apps
    ```

    Be sure to have Python 3.8 installed—if you use [pyenv](https://github.com/pyenv/pyenv#readme), simply run:

    ```shell
    pyenv install 3.8
    ```

1.  Clone your fork locally and install dependencies.

    ```shell
    git clone https://github.com/your-username/autorefine path/to/autorefine
    cd path/to/autorefine
    poetry env use $(cat .python-version)
    poetry install
    ```

    Next up, simply activate the virtual environment and install pre-commit hooks:

    ```shell
    poetry shell
    pre-commit install --hook-type pre-commit --hook-type pre-push
    ```

For more information on how to contribute, check out [CONTRIBUTING.md](https://github.com/bswck/autorefine/blob/HEAD/CONTRIBUTING.md).<br/>
Always happy to accept contributions! ❤️


# Legal info
© Copyright by Bartosz Sławecki ([@bswck](https://github.com/bswck)).
<br />This software is licensed under the terms of [GPL-3.0 License](https://github.com/bswck/autorefine/blob/HEAD/LICENSE).
