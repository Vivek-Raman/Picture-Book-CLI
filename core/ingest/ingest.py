import os
from pathlib import Path
import click

from core.db import db
from .metadata import extract_metadata
from core.models import MediaItem


def do_ingest(directory: Path) -> None:
    # find all picutres recursively

    for root, _, files in directory.walk():
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp",
                                      ".tiff", ".webp", ".heic", ".mov")):
                _ingest_media(root / file)
    pass


def _ingest_media(file: Path) -> None:
    click.echo(f"Ingesting media: {file}")

    metadata = extract_metadata(file)

    # TODO: extract thumbnail if available
    # TODO: generate thumbnail if not available
    # thumbnail = _extract_thumbnail(file)

    # save media item to database
    media_item = MediaItem(
        path=file,
        date_taken=metadata.get("date_taken"),
        # location=metadata.get("location"),
        # thumbnail=thumbnail,
        # tags=metadata.get("tags"),
    )
    with db() as conn:
        conn.execute(
            "INSERT INTO media_items (path, date_taken) VALUES (?, ?)",
            (media_item.path, media_item.date_taken.isoformat()))
        conn.commit()

    click.echo(f"Media item saved: {media_item}")
