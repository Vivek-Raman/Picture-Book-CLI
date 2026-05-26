import click
from core.ingest import do_ingest
from core.db import init_db
from pathlib import Path


@click.group()
@click.version_option(version="1.0.0", prog_name="picture-book")
def cli() -> None:
    """Picture Book command-line tools."""
    init_db()


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
def ingest(directory: str) -> None:
    """Ingests pictures from a new directory."""
    do_ingest(Path(directory))


if __name__ == "__main__":
    cli()
