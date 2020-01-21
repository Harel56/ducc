import click

from .reader import Reader
from .utils import Connection, Hello, Config, Snapshot


'''def upload_thought(address, user_id, thought):
    th = Thought(user_id, datetime.today(), thought)
    with Connection.connect(*address) as conn:
        conn.send(th.serialize())
'''


def upload_sample(host, port, path):
    """same as run_client"""
    run_client(host, port, path)


def run_client(host, port, sample):
    """
    Runs the client connecting to the address given by arguments 'host', 'port';
    reading data from file given by sample.
    sample argument may be either a file object or a path

    example:
    >>>sample = open('sample.mind')
    >>>run_client(('127.0.0.1', 8000), sample)
    """
    reader = Reader(sample)
    for snapshot in reader:
        with Connection.connect(host, port) as connection:
            hello_msg = Hello(reader.user.user_id, reader.user.username, reader.user.birthday, reader.user.gender)
            connection.send_message(hello_msg.serialize())
            config_msg = Config.deserialize(connection.receive_message())
            optional = {'translation':snapshot.translation, 'rotation':snapshot.rotation, 'hunger':snapshot.hunger, 'thirst':snapshot.thirst, 'happiness':snapshot.happiness}
            snapshot_msg = Snapshot(snapshot.timestamp, snapshot.color, snapshot.depth,
                                    **{key: value for (key, value) in optional.items() if (key in config_msg.fields)})
            connection.send_message(snapshot_msg.serialize())


def convert(info):
    """converts data structure given by reader to format matching the protocol with the server"""
    return info


@click.command()
@click.option('--host', default='localhost', help="Host to connect to")
@click.option('--port', default=8000, help="Host's port")
@click.argument('file', type=click.File('rb'), help="File to read from")
def client(host, port, file):
    """
    Runs the client connecting to server at address given by options '--host', '--port';
    reading data sample from given file argument.
    """
    run_client(host, port, file)


if __name__ == '__main__':
    client()
