import click
from .site import run_server as start


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', default='localhost', show_default=True)
@click.option('-p', '--port', default=8080, show_default=True, help="Port to listen on")
@click.option('-d', '--database', default='mongodb://localhost:27017/', show_default=True, help="url for the database")
def run_server(host, port, database):
    start(host, port, database)


cli(prog_name="python -m ducc.gui")
