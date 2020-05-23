import click
import itertools
from .reader import Reader
from .utils import Connection, protocol, net


def upload_sample(host, port, path, limit=None):
    """same as run_client"""
    run_client(host, port, path, limit)


def run_client(host, port, sample, limit=None):
    """
    Runs the client connecting to the address given by arguments 'host', 'port';
    reading data from file given by sample.
    sample argument may be either a file object or a path

    example:
    >>>sample = open('sample.mind')
    >>>run_client('localhost', 8000, sample)
    """
    with Reader(sample) as reader:
        for snapshot in itertools.islice(reader, limit):
            with Connection.connect(host, port) as connection:
                hello_msg, snapshot_msg = convert(reader.user, snapshot)
                connection.send_message(hello_msg)
                _ = protocol.Config.deserialize(connection.receive_message())
                connection.send_message(snapshot_msg)


def convert(user, snapshot):
    """converts data structure given by reader to format matching the protocol with the server"""
    return protocol.Hello(user.user_id, user.username, user.birthday, "mfo"[user.gender]).serialize(), \
           snapshot.SerializeToString()


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.option('-h', '--host', default='localhost', show_default=True, help="Host to connect to")
@click.option('-p', '--port', type=click.IntRange(0, 0xffff), default=8000, show_default=True, help="Host's port")
@click.option('-l', '--limit', type=click.IntRange(0), help="optional limit to the amount of snapshots to read and "
                                                            "upload")
@click.argument('file', type=click.File('rb'))
def client(host, port, limit, file):
    """
    Runs the client connecting to server at address given by options '--host', '--port';
    reading data sample from given file argument.
    """
    with net.SafetyNet():
        run_client(host, port, file, limit)


if __name__ == '__main__':
    cli(prog_name="python -m ducc.client")
