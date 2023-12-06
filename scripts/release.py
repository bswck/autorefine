#!/usr/bin/env python
# (C) 2023–present Bartosz Sławecki (bswck)
#
# Note:
# If you want to change this file, you might want to do it at the infrastructure
# level. See https://github.com/bswck/skeleton.
"""
Automate the release process by updating local files, creating and pushing a new tag.

The complete the release process, create a GitHub release.
GitHub Actions workflow will publish the package to PyPI via Trusted Publisher.

Usage:
$ poe release [major|minor|patch|MAJOR.MINOR.PATCH]
"""
from __future__ import annotations

import argparse
import functools
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


def _decode_if_bytes(value: bytes | str, /) -> str:
    """Decode bytes to str."""
    if isinstance(value, bytes):
        return value.decode()
    return value


def _setup_logging() -> None:
    _LOGGER.setLevel(logging.INFO)
    _logger_handler = logging.StreamHandler()
    _logger_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    _LOGGER.addHandler(_logger_handler)


def release(version: str, /) -> None:
    """Release a semver version."""
    cmd, shell = str.split, functools.partial(subprocess.run, check=True)

    changed_files = _decode_if_bytes(
        shell(
            cmd("git diff --name-only HEAD"),
            capture_output=True,
        ).stdout
    )

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

    shell([*cmd("poetry version"), version])

    new_version = "v" + (
        _decode_if_bytes(
            shell(
                cmd("poetry version --short"),
                capture_output=True,
            ).stdout,
        ).strip()
    )

    default_release_notes = _decode_if_bytes(
        shell(
            cmd(f"towncrier build --draft --yes --version={new_version}"),
            capture_output=True,
        ).stdout
    )
    shell(cmd(f"towncrier build --yes --version={new_version}"))

    changed_for_release = _decode_if_bytes(
        shell(
            cmd("git diff --name-only HEAD"),
            capture_output=True,
        ).stdout
    )

    if changed_for_release:
        shell(cmd("git diff"))
        do_commit = _ask_for_confirmation(
            "You are about to commit and push auto-changed files due "
            "to version upgrade, see the diff view above. "
            "Are you sure?",
            default=True,
        )

        if do_commit:
            shell([*cmd("git commit -am"), f"Release {new_version}"])
            shell(cmd("git push"))
        else:
            _abort(
                "Changes made uncommitted. "
                "Commit your unrelated changes and try again.",
            )

    _LOGGER.info("Creating %s tag...", new_version)

    try:
        shell([*cmd("git tag -sa"), new_version, "-m", f"Release {new_version}"])
    except subprocess.CalledProcessError:
        _abort(f"Failed to create {new_version} tag, probably already exists.")
    else:
        _LOGGER.info("Pushing local tags...")
        shell(cmd("git push --tags"))

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
                shell(cmd(f"{_EDITOR} {temp_file.name}"))
                release_notes = Path(temp_file.name).read_text()
                print("Release notes:")
                print(release_notes)
                print()
                notes_complete = _ask_for_confirmation(
                    "Do you confirm the release notes?",
                    default=True,
                )

            shell(
                cmd(
                    f"gh release create {new_version} --generate-notes "
                    f"--notes-file {temp_file.name}",
                )
            )
            os.unlink(temp_file.name)
        else:
            shell(cmd(f"gh release create {new_version} --generate-notes"))


def main(argv: list[str] | None = None) -> None:
    """Run the script."""
    _setup_logging()

    parser = argparse.ArgumentParser(description="Release a semver version.")
    parser.add_argument(
        "version",
        type=str,
        nargs=1,
    )
    args: argparse.Namespace = parser.parse_args(argv)
    release(args.version.pop())


if __name__ == "__main__":
    main()
