import click
import requests

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


@cli.command('get-users')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
def get_users(host, port):
    response = requests.get(f'http://{host}:{port}/users')
    click.echo(response.json())


@cli.command('get-user')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
@click.argument('user-id', type=click.INT)
def get_user(host, port, user_id):
    response = requests.get(f'http://{host}:{port}/users/{user_id}')
    click.echo(response.json())


@cli.command('get-snapshots')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
@click.argument('user-id', type=click.INT)
def get_snapshots(host, port, user_id):
    response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots')
    click.echo(response.json())


@cli.command('get-snapshot')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
@click.argument('user-id', type=click.INT)
@click.argument('snapshot-id', type=click.INT)
def get_snapshot(host, port, user_id, snapshot_id):
    response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}')
    click.echo(response.json())


@cli.command('get-result')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
@click.option('-s', '--save', type=click.File('w'), help="file to save result's data to")
@click.argument('user-id', type=click.INT)
@click.argument('snapshot-id', type=click.INT)
@click.argument('result-name')
def get_result(host, port, save, user_id, snapshot_id, result_name):
    response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}')
    click.echo(response.json(), file=save)


if __name__ == "__main__":
    cli()
