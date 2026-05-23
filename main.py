import click


@click.group()
@click.version_option(version="1.0.0", prog_name="picture-book")
def cli() -> None:
    """Picture Book command-line tools."""


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
def ingest(directory: str) -> None:
    """Ingests pictures from a new directory."""
    click.echo(f"Ingesting a new picture book from {directory}...")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
