import click
from .reader import Reader
from .utils import Connection, Hello, Config


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
    >>>run_client(('localhost', 8000), sample)
    """
    reader = Reader(sample)
    for snapshot in reader:
        with Connection.connect(host, port) as connection:
            hello_msg, snapshot_msg = convert(reader.user, snapshot)
            connection.send_message(hello_msg)
            config_msg = Config.deserialize(connection.receive_message())
            connection.send_message(snapshot_msg)


def convert(user, snapshot):
    """converts data structure given by reader to format matching the protocol with the server"""
    return Hello(user.user_id, user.username, user.birthday, "mfo"[user.gender]).serialize(), snapshot.SerializeToString()


@click.command()
@click.option('-h', '--host', default='localhost', help="Host to connect to")
@click.option('-p', '--port', default=8000, help="Host's port")
@click.argument('file', type=click.File('rb'))
def client(host, port, file):
    """
    Runs the client connecting to server at address given by options '--host', '--port';
    reading data sample from given file argument.
    """
    run_client(host, port, file)


if __name__ == '__main__':
    client()
