from __future__ import annotations

import importlib
from contextvars import Context, ContextVar, copy_context
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from autorefine import __version__
from autorefine.settings import SETTINGS_PATHS, AppSettings, cascade_load_settings


@dataclass
class AppContext:
    app: App
    repository: Path
    dry_run: bool
    settings: AppSettings
    verbose: bool


_app_context: ContextVar[AppContext] = ContextVar("_app_context")


class App(typer.Typer):
    def __init__(
        self,
        runtime_context: Context | None = None,
        stdout_prefix: str = "[italic]autorefine[/italic][bold][purple]>[/purple]",
        stderr_prefix: str = "[italic]autorefine[/italic][bold][red]>[/red]",
    ) -> None:
        super().__init__(
            name="autorefine",
            invoke_without_command=True,
            no_args_is_help=True,
        )
        self._initializing = True
        if runtime_context is None:
            runtime_context = copy_context()
        self.runtime_context = runtime_context
        self.stdout = Console()
        self.stdout_prefix = stdout_prefix
        self.stderr = Console(stderr=True)
        self.stderr_prefix = stderr_prefix

    def echo(
        self,
        *args: object,
        sep: str = " ",
        end: str = "\n",
        verbose: bool = False,
    ) -> None:
        if not verbose or verbose and not self._initializing and self.context.verbose:
            return self.stdout.print(
                self.stdout_prefix,
                *args,
                sep=sep,
                end=end,
                highlight=False,
            )

    def error(
        self,
        *args: object,
        sep: str = " ",
        end: str = "\n",
    ) -> None:
        return self.stderr.print(
            self.stderr_prefix,
            *args,
            sep=sep,
            end=end,
            highlight=False,
        )

    @property
    def context(self) -> AppContext:
        return _app_context.get()  # fails on self._initializing=True

    def __call__(self) -> None:
        self.info.callback = global_options
        return self.runtime_context.run(super().__call__)


app = App()


@app.command()
def analyze() -> None:
    """Analyze the project with configured linters and type checkers."""


@app.command()
def autopilot() -> None:
    """Apply automatic fixes and commit them in chunks."""


@app.command()
def ci() -> None:
    """Run tests, snipe regressions."""


@app.command()
def pr() -> None:
    """Create a PR at the end of autorefine's iteration."""


@app.command()
def roadmap() -> None:
    """Create a refactoring roadmap for autorefine's iteration."""


@app.command()
def troubleshoot() -> None:
    """Find a commit that caused regression."""


def handle_version(version: bool, short: bool) -> None:
    if version:
        if short:
            print(__version__)
        else:
            app.echo(__version__)
        raise typer.Exit()
    if short:
        raise typer.BadParameter("--short is only valid when combined with --version")


def import_apis() -> None:
    app.echo("Importing tool APIs...", verbose=True)
    counter = 0

    for module_name in app.context.settings.tool_apis:
        tool_api = importlib.import_module(module_name)
        app.echo(
            f"Imported [bold]{module_name}[/bold] "
            f"(new tool(s): [bold]{', '.join(tool_api.tools)}[/bold])",
            verbose=True,
        )
        counter += 1

    app.echo(f"Unlocked {counter} tool(s).", verbose=True)


def global_options(
    repository: Annotated[
        Path,
        typer.Option("-R", "--repository", help="Path to repository."),
    ] = Path("."),
    config: Annotated[
        Path,
        typer.Option(
            "-C",
            "--configuration",
            help="Custom configuration file to load (TOML).",
        ),
    ] = Path("autorefine.toml"),
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Enable dry run mode (no filesystem writes)."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "-v",
            "--verbose",
            help="Enable verbose mode (more informational messages).",
        ),
    ] = False,
    version: Annotated[
        bool,
        typer.Option("--version", help="Display autorefine's version and exit."),
    ] = False,
    short: Annotated[
        bool,
        typer.Option(
            "--short",
            help="Shorten autorefine's displayed version (only with --version).",
        ),
    ] = False,
) -> None:
    handle_version(version, short)
    settings_paths = None

    if config:
        settings_paths = SETTINGS_PATHS.copy()
        settings_paths[config]

    _app_context.set(
        AppContext(
            app=app,
            repository=repository,
            dry_run=dry_run,
            settings=cascade_load_settings(settings_paths),
            verbose=verbose,
        )
    )
    app._initializing = False

    import_apis()


if __name__ == "__main__":
    app()
