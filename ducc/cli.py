import click
import requests


@click.group()
def cli():
    pass


@cli.command('get-users')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
def get_users(host, port):
    response = requests.get(f'http://{host}:{port}/users')
    click.echo(response.text)


@cli.command('get-user')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
@click.argument('user-id', type=click.INT)
def get_user(host, port, user_id):
    response = requests.get(f'http://{host}:{port}/users/{user_id}')
    click.echo(response.text)


@cli.command('get-snapshots')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
@click.argument('user-id', type=click.INT)
def get_snapshots(host, port, user_id):
    response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots')
    click.echo(response.text)


@cli.command('get-snapshot')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
@click.argument('user-id', type=click.INT)
@click.argument('snapshot-id')
def get_snapshot(host, port, user_id, snapshot_id):
    response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}')
    click.echo(response.text)


@cli.command('get-result')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000, help="Port to listen on")
@click.option('-s', '--save', type=click.File('w'), help="file to save result's data to")
@click.argument('user-id', type=click.INT)
@click.argument('snapshot-id')
@click.argument('result-name')
def get_result(host, port, save, user_id, snapshot_id, result_name):
    response = requests.get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}')
    click.echo(response.text, file=save)


if __name__ == "__main__":
    cli()
