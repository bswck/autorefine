#!/usr/bin/env python
# (C) 2023–present Bartosz Sławecki (bswck)
#
# This file was generated from bswck/skeleton@01e08d2.
# Instead of changing this particular file, you might want to alter the template:
# https://github.com/bswck/skeleton/tree/01e08d2/project/scripts/release.py.jinja
#
"""
Automate the release process by updating local files, creating and pushing a new tag.

The complete the release process, create a GitHub release.
GitHub Actions workflow will publish the package to PyPI via Trusted Publisher.

Usage:
$ poe release [major|minor|patch|MAJOR.MINOR.PATCH]
"""
from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path


_LOGGER = logging.getLogger("release")
_EDITOR = os.environ.get("EDITOR", "vim")


def _abort(msg: str, /) -> None:
    """Display an error message and exit the script process with status code -1."""
    _LOGGER.critical(msg)
    sys.exit(-1)


def _ask_for_confirmation(msg: str, *, default: bool | None = None) -> bool:
    """Ask for confirmation."""
    if default is None:
        msg += " (y/n): "
        default_answer = None
    elif default:
        msg += " (Y/n): "
        default_answer = "y"
    else:
        msg += " (y/N): "
        default_answer = "n"

    answer = None
    while answer is None:
        answer = input(msg).casefold().strip() or default_answer
    return answer[0] == "y"


def _setup_logging() -> None:
    _LOGGER.setLevel(logging.INFO)
    _logger_handler = logging.StreamHandler()
    _logger_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    _LOGGER.addHandler(_logger_handler)


def release(version: str, /) -> None:
    """Release a semver version."""
    command, run = (
        subprocess.getoutput,
        lambda prompt: subprocess.run(*prompt, check=True),
    )

    changed_files = command("git status --porcelain")

    if changed_files:
        do_continue = _ask_for_confirmation(
            "There are uncommitted changes in the working tree in these files:\n"
            f"{changed_files}\n"
            "Continue? They will be included in the release commit.",
            default=False,
        )
        if not do_continue:
            _abort("Uncommitted changes in the working tree.")

    # If we get here, we should be good to go
    # Let's do a final check for safety
    do_release = _ask_for_confirmation(
        f"You are about to release {version!r} version. Are you sure?",
        default=True,
    )

    if not do_release:
        _abort(f"You said no when prompted to bump to the {version!r} version.")

    _LOGGER.info("Bumping to the %r version", version)
    run("poetry", "version", version)

    new_version = "v" + command("poetry version --short").strip()
    default_release_notes = command(
        f"towncrier build --draft --yes --version={new_version}"
    )
    command(f"towncrier build --yes --version={new_version}")

    changed_for_release = command("git status --porcelain")
    if changed_for_release:
        run("git", "diff")

        do_commit = _ask_for_confirmation(
            "You are about to commit and push auto-changed files due "
            "to version upgrade, as in the diff view displayed just now. "
            "Are you sure?",
            default=True,
        )

        if do_commit:
            run("git", "commit", "-am", f"Release {new_version}")
            run("git", "push")
        else:
            _abort(
                "Changes made uncommitted. "
                "Commit your unrelated changes and try again.",
            )

    _LOGGER.info("Creating %s tag...", new_version)

    try:
        run("git", "tag", "-sa", new_version, "-m", f"Release {new_version}")
    except subprocess.CalledProcessError:
        _abort(f"Failed to create {new_version} tag, probably already exists.")
    else:
        _LOGGER.info("Pushing local tags...")
        run("git", "push", "--tags")

    do_release = _ask_for_confirmation(
        "Create a GitHub release now? GitHub CLI required.",
        default=True,
    )

    if do_release:
        do_write_notes = _ask_for_confirmation(
            "Do you want to write release notes?",
            default=True,
        )

        if do_write_notes:
            notes_complete = False
            release_notes = default_release_notes
            temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
            temp_file.write(release_notes)
            temp_file.close()

            while not notes_complete:
                run(_EDITOR, temp_file.name)
                release_notes = Path(temp_file.name).read_text()
                print("Release notes:")
                print(release_notes)
                print()
                notes_complete = _ask_for_confirmation(
                    "Do you confirm the release notes?",
                    default=True,
                )

            run(
                "gh", "release", "create", new_version, "--generate-notes",
                "--notes-file", temp_file.name,
            )
            os.unlink(temp_file.name)
        else:
            run("gh", "release", "create", new_version, "--generate-notes")


def main(argv: list[str] | None = None) -> None:
    """Run the script."""
    _setup_logging()

    parser = argparse.ArgumentParser(description="Release a semver version.")
    parser.add_argument("version", type=str)
    release(*vars(parser.parse_args(argv)).values())


if __name__ == "__main__":
    main()
