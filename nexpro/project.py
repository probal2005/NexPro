"""NexPro project manifest and starter files."""

import json
import tomllib
from pathlib import Path

from nexpro.errors import NexProError


MANIFEST = "nexpro.toml"


class Project:
    def __init__(self, manifest):
        self.root = manifest.parent.resolve()
        try:
            config = tomllib.loads(manifest.read_text(encoding="utf-8"))["project"]
            self.entry = self._path(config["entry"])
            self.tests = self._path(config.get("tests", "tests"))
        except (AttributeError, TypeError, KeyError, ValueError, OSError) as error:
            raise NexProError(f"Invalid project manifest {manifest}: {error}") from error

    def _path(self, name):
        relative = Path(name)
        target = (self.root / relative).resolve()
        if relative.is_absolute() or not target.is_relative_to(self.root):
            raise ValueError("Project paths must stay inside the project directory")
        return target


def find_project(directory=None):
    current = (directory or Path.cwd()).resolve()
    for folder in (current, *current.parents):
        manifest = folder / MANIFEST
        if manifest.is_file():
            return Project(manifest)
    return None


def init_project(directory):
    directory.mkdir(parents=True, exist_ok=True)
    content = {
        directory / MANIFEST: (
            f"[project]\nname = {json.dumps(directory.resolve().name, ensure_ascii=False)}\n"
            'entry = "main.pa"\ntests = "tests"\n'
        ),
        directory / "main.pa": 'say "Hello NexPro!"\n',
    }
    created = []
    try:
        for path, source in content.items():
            with path.open("x", encoding="utf-8") as file:
                created.append(path)
                file.write(source)
    except OSError as error:
        for path in created:
            path.unlink(missing_ok=True)
        raise NexProError(f"Could not initialize {directory}: {error}") from error
