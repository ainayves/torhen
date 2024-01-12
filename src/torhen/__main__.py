"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Torhen."""


if __name__ == "__main__":
    main(prog_name="torhen")  # pragma: no cover
