import click
import pathlib
import threading
from .utils import Listener, Hello, Config, Snapshot
from .parsers import parse_translation, parse_color_image


class Context:
    def __init__(self, root, lock):
        self.root = root
        self.lock = lock

    def path(self, file_name=''):
        return self.root / file_name

    def save(self, file_name, data):
        with self.path(file_name).open('w') as f:
            f.write(data)


def handle_connection(connection, callback):
    with connection:
        hello = Hello.deserialize(connection.receive_message())
        config = Config('translation', 'color_image')
        connection.send_message(config.serialize())
        snapshot = Snapshot.deserialize(connection.receive_message())
    callback((hello, snapshot))


def run_server(host, port, publish):
    """
    Runs the server with the given address,
    using publish as callback giving it the received messages.

    example:
    >>> run_server('127.0.0.1', 8000, print)
    """
    listener = Listener(host, port)
    listener.start()
    while True:
        client = listener.accept()
        threading.Thread(target=handle_connection, args=(client, publish)).start()


def publisher(publish):
    """Decorator"""
    def decorator(*args, **kwargs):
        def wrapper(msg):
            return publish(msg, *args, **kwargs)
        return wrapper
    return decorator


@publisher
def publish_to_data_dir(message, data_dir, lock=threading.Lock()):
    user, snapshot = message
    dt = snapshot.datetime()
    user_dir = data_dir / str(user.user_id)
    dir_path = user_dir / ("%04d-%02d-%02d_%02d-%02d-%02d-%06d" % (
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond))
    with lock:
        user_dir.mkdir(exist_ok=True)
        dir_path.mkdir(exist_ok=True)
    context = Context(dir_path, lock)
    parse_translation(context, snapshot)
    parse_color_image(context, snapshot)


def publish_to_queue():
    pass


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', default=8000, help="Port to listen on")
@click.argument('url')
def server(host, port, url):
    pass


if __name__ == '__main__':
    server()
