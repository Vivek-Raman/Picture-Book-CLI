from __future__ import annotations

import json
import click
from fractions import Fraction
from typing import Any
from pathlib import Path
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def _serialize_exif_value(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, tuple):
        return [_serialize_exif_value(item) for item in value]
    if isinstance(value, Fraction):
        return float(value)
    if hasattr(value, "numerator") and hasattr(value, "denominator"):
        return float(value)
    return value


def _extract_exif(image: Image.Image) -> dict[str, Any]:
    exif = image.getexif()
    if not exif:
        return {}

    exif_data: dict[str, Any] = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_data[str(tag)] = _serialize_exif_value(value)

    gps_ifd = exif.get_ifd(0x8825)
    if gps_ifd:
        exif_data["GPSInfo"] = {
            str(GPSTAGS.get(tag_id, tag_id)): _serialize_exif_value(value)
            for tag_id, value in gps_ifd.items()
        }

    return exif_data


def extract_metadata(file: Path) -> dict:
    try:
        with Image.open(file.absolute().as_posix()) as image:
            exif_data = _extract_exif(image)
    except OSError as exc:
        click.echo(f"No EXIF data for {file}: {exc}")
        return {}

    if not exif_data:
        click.echo(f"No EXIF data for {file}")
        return {}

    click.echo("Keys:")
    click.echo(exif_data.keys())

    click.echo(f"EXIF data for {file}:")
    click.echo(json.dumps(exif_data, indent=2, default=str))
    return {}
