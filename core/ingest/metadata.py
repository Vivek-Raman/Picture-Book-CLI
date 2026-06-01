from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import click

DATE_TAGS = (
    "DateTimeOriginal",
    "CreateDate",
    "MediaCreateDate",
    "TrackCreateDate",
    "DateTimeDigitized",
    "ModifyDate",
)

_DATE_RE = re.compile(
    r"(\d{4})[:-](\d{2})[:-](\d{2})[ T](\d{2}):(\d{2}):(\d{2})")


def extract_metadata(file: Path) -> dict:
    metadata = _run_exiftool(file)
    if not metadata:
        click.echo(f"No metadata for {file}")
        return {}

    click.echo(f"Metadata for {file}:")
    click.echo(json.dumps(metadata, indent=2, default=str))

    date_taken = _extract_date_taken(metadata)
    if date_taken is None:
        click.echo(f"No capture date for {file}")
        return {}

    return {"date_taken": date_taken}


def _parse_exif_date(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value)
    match = _DATE_RE.match(str(value).strip())
    if not match:
        return None
    year, month, day, hour, minute, second = map(int, match.groups())
    return datetime(year, month, day, hour, minute, second)


def _run_exiftool(file: Path) -> dict[str, Any]:
    exiftool = shutil.which("exiftool")
    if not exiftool:
        click.echo(
            "exiftool not found on PATH; install with: brew install exiftool",
            err=True,
        )
        return {}

    result = subprocess.run(
        [exiftool, "-json", file.absolute().as_posix()],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        click.echo(f"exiftool failed for {file}: {stderr}", err=True)
        return {}

    records = json.loads(result.stdout)
    if not records:
        return {}
    return records[0]


def _extract_date_taken(metadata: dict[str, Any]) -> datetime | None:
    for tag in DATE_TAGS:
        date_taken = _parse_exif_date(metadata.get(tag))
        if date_taken is not None:
            return date_taken
    return None
