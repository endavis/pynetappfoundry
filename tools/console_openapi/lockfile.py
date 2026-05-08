"""Reproducibility lockfile for the generated OpenAPI spec."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Lockfile:
    """Metadata captured at generation time."""

    repo: str
    requested_ref: str
    resolved_sha: str
    tool_version: str
    services: tuple[str, ...]
    endpoint_count: int

    def to_json(self) -> str:
        data = asdict(self)
        data["services"] = list(self.services)
        return json.dumps(data, indent=2, sort_keys=True) + "\n"

    @classmethod
    def from_json(cls, text: str) -> Lockfile:
        data = json.loads(text)
        return cls(
            repo=data["repo"],
            requested_ref=data["requested_ref"],
            resolved_sha=data["resolved_sha"],
            tool_version=data["tool_version"],
            services=tuple(data["services"]),
            endpoint_count=int(data["endpoint_count"]),
        )

    def write(self, path: Path) -> None:
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def read(cls, path: Path) -> Lockfile:
        return cls.from_json(path.read_text(encoding="utf-8"))
