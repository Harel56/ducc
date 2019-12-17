import click

from .client import run_client
from .server import run_server
from .reader import Reader


@click.group()
def cli():
    pass


@cli.command()
@click.option('--limit', default=-1, help="Limit the amount of snapshots to read and print, defaults to no limit")
@click.argument('filename', type=click.Path())
def read(limit, filename):
    """Makes a Reader object for the given file, And prints its representation."""
    reader = Reader(filename)
    click.echo(str(reader))
    if limit < 0:
        return
    for snapshot in reader:
        click.echo(str(snapshot))
        limit -= 1
        if not limit:
            break


@cli.command()
@click.argument('address', help="Address to connect to")
@click.argument('file', type=click.File('rb'), help="File to read from")
def client(address, file):
    """Runs the client"""
    address = address.split(':', 1)
    run_client((address[0], int(address[1])), file)


@cli.command()
@click.argument('address', help="Address to listen on")
@click.argument('data_dir')
def server(address, data_dir):
    """Runs the Server"""
    address = address.split(':', 1)
    run_server((address[0], int(address[1])), data_dir)


if __name__ == "__main__":
    cli()
