import click
from .site import run_server as start


@click.command()
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=8080)
@click.option('-d', '--database')
def run_server(host, port, database):
    start(host, port, database)
