from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, Protocol

import tomli
from pydantic import AfterValidator, AliasPath, BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from typing_extensions import Self


class SettingsReader(Protocol):
    def __init__(self, **settings: Any) -> None: ...
    def read_settings(self) -> AppSettings | None: ...
    def model_dump(self) -> dict[str, Any]: ...


class AppSettings(BaseModel):
    tool_apis: Annotated[
        list[Annotated[str, AfterValidator(str.casefold)]],
        Field(default_factory=list),
    ]

    def read_settings(self) -> Self:
        return self


class SettingsFromPyproject(BaseModel):
    settings: Annotated[
        AppSettings | None,
        Field(validation_alias=AliasPath("tool", "autorefine")),
    ] = None

    model_config = ConfigDict(extra="ignore")

    def read_settings(self) -> AppSettings | None:
        return self.settings


SETTINGS_PATHS: dict[Path, type[SettingsReader]] = defaultdict(
    lambda: AppSettings,
    {
        Path("pyproject.toml"): SettingsFromPyproject,
        Path("autorefine.toml"): AppSettings,
    },
)


def cascade_load_settings(
    paths: dict[Path, type[SettingsReader]] | None = None,
) -> AppSettings:
    if paths is None:
        paths = SETTINGS_PATHS
    data: dict[str, Any] = {}
    for path, reader_class in paths.items():
        try:
            reader = reader_class(**tomli.loads(path.read_text()))
        except FileNotFoundError:
            continue
        settings = reader.read_settings()
        if not settings:
            continue
        data |= settings.model_dump()
    return AppSettings(**data)
