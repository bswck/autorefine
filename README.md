
# autorefine [![Package version](https://img.shields.io/pypi/v/autorefine?label=PyPI)](https://pypi.org/project/autorefine/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/autorefine.svg?logo=python&label=Python)](https://pypi.org/project/autorefine/)
[![Tests](https://github.com/bswck/autorefine/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/autorefine/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/autorefine.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/autorefine)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?label=Code%20style)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/bswck/autorefine.svg?label=License)](https://github.com/bswck/autorefine/blob/HEAD/LICENSE)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Mechanize the refactoring process to operate on a large scale.

The project is aimed to provide a framework for the process of refactoring Python projects
from the very beginning to the very end:
- `autorefine analyze` → **analyze the project** with linters and type checkers,
- `autorefine roadmap` → **create a refactoring roadmap** (like https://github.com/CERT-Polska/malduck/issues/110, but with more details available as a specialized document),
- `autorefine plan` → **create a delivery plan** (like in the issue above) to split the refactoring process into **a sequence of iterations**,
- `autorefine autopilot` → **apply automatic fixes** and commit them in reviewable and git-bisectable chunks with meaningful descriptions,
- `autorefine audit` → typically **run tests** and other tools that determine whether the project runs safe,
- `autorefine troubleshoot` → using the configured **auditing task**, `git bisect` to **find out what fix went wrong**, describe the problem,
- leave the rest for manual work,
- `autorefine finalize` → **create a PR** (like https://github.com/CERT-Polska/malduck/issues/111) to finalize the current iteration of refactoring with a detailed description of the changes and a link to the roadmap, delivery plan and all commits.

Created to accomplish https://github.com/jaraco/skeleton/issues/98 and for personal use to raise awareness of best practices across the Python community globally.

# Planned tooling
The project is planned to be a wrapper around the following well-tested & recognized tools:
- [MonkeyType](https://github.com/Instagram/MonkeyType#readme) for automatic type annotations generation,
- [Fixit](https://github.com/Instagram/Fixit#readme) for automatic fixes that require static analysis and scope analysis and planning of manual refactoring steps,
- [Ruff](https://github.com/astral-sh/ruff#readme) for automatic fixes and planning of manual refactoring steps,
- Static type checking:
  - [mypy](https://github.com/python/mypy#readme),
  - [pyre](https://github.com/facebook/pyre-check#readme),
  - [pytype](https://github.com/google/pytype#readme),
- [diff-cover](https://github.com/Bachmann1234/diff_cover#readme) for [coverage](https://github.com/nedbat/coverage#readme) reports on fixes,
- [smokeshow](https://github.com/samuelcolvin/smokeshow#readme) for hosting detailed refactoring roadmaps and delivery plans,
- [pandas](https://github.com/pandas-dev/pandas) for collecting tasks and creating markdown tables,
- [GitHub CLI](https://cli.github.com/) for creating tickets.

# Refactoring workflow
`autorefine` will be a CLI tool that will help you refactor a project in a few simple steps:

1. Fork a repository you want to refactor.

1. Create a new branch for refactoring.

1. Run `autorefine configure` to run a wizard that will help you configure `autorefine`, configure audits (`autorefine` will typically detect doctest, pytest and other tools that determine whether the project runs safe) and refactor the project for a specific choice of linting tools.

1. Run `autorefine analyze` to analyze the project with linters and type checkers. `autorefine` now knows what needs to be fixed in the current HEAD.

1. Run `autorefine roadmap` to create a refactoring roadmap. You will have a checklist of all the things that need to be fixed in the project automatically and manually.

2. Run `autorefine plan` to create a delivery plan and set up iterations of the refactoring process. For example, you can start off by a PR that aims to modernize the codebase and does not change the implementation (fixes in the roadmap will be grouped and you will be able to select which ones you want to apply in this iteration), that would be the first iteration, and then apply some implementation-changing autofixes, such as replacing `f"'{x}'"` with `f"{x!r}"`—that could be the second iteration. Having a delivery plan will make `autorefine` create a PR for each iteration, so that you can review the changes and merge them separately.

3. Run `autorefine autopilot` to apply automatic fixes and commit them in reviewable and git-bisectable chunks with meaningful descriptions.

4. Run `autorefine audit` to prevent future regressions.

5. Run `autorefine troubleshoot` to repeatedly call `autorefine audit` within `git bisect` to find out what fix went wrong, and get a detailed description of the problem and suggestions on how to fix it.

6. Manually fix the problems that cannot be fixed automatically. You will find them in the roadmap (`autorefine roadmap`).

7. Run `autorefine finalize` to finalize the current iteration and create a PR with a detailed description of the changes and a link to the roadmap, delivery plan and all commits of the current refactor iteration.

# Non-MVP ideas
- `autorefine ci` to create a dedicated CI pipeline (which will, by default, run `autorefine analyze` and `autorefine audit` on every PR) for your Git hosting provider (GitHub, GitLab, Bitbucket, etc.),
- `autorefine template [TEMPLATE_NAME]` to configure Quality Assurance and CI/CD tooling (Ruff, tox, towncrier, Sphinx, etc.) by smart copying what is seen a specified repository (e.g. `autorefine template jaraco/skeleton`+[jaraco.develop](https://github.com/jaraco/jaraco.develop) could be used to copy tox.ini, GitHub Actions etc.)—feature for projects that don't intend to use a skeleton.
- `autorefine breakdown` to create separate tickets for each fix in the roadmap in your workflow management tool (GitHub Projects, Jira, ClickUp, Asana, Trello, etc.).

# Get inspired
- https://instagram-engineering.com/static-analysis-at-scale-an-instagram-story-8f498ab71a0c

# Installation
If you want to…



## …use this tool in your project 💻
You might simply install it with [pipx](https://github.com/pypa/pipx#readme):

```shell
pipx install autorefine
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
