import click
import json
import logging
import pathlib
import struct
import threading
from urllib.parse import urlparse
from . import cortex_pb2
from .utils import Listener, protocol, queue, net


class Context:
    def __init__(self, root, lock):
        self.root = root
        self.lock = lock

    def path(self, file_name=''):
        return self.root / file_name

    def save(self, file_name, data):
        with self.path(file_name).open('w') as f:
            f.write(data)


def handle_connection(connection, callback, log=True):
    with connection:
        if log:
            logging.info("Received connection on " + str(connection))
        try:
            message = read_message(connection)
        except Exception as exc:
            if log:
                logging.warning(f"Failed to read message from {connection}: {exc}")
            return 1
    try:
        callback(message)
    except Exception as exc:
        if log:
            logging.warning("Failed publishing snapshot:" + str(exc))
        return 1
    if log:
        logging.info("Published snapshot successfully")


def read_message(connection):
    hello = protocol.Hello.deserialize(connection.receive_message())
    config = protocol.Config('pose', 'color_image', 'depth_image', 'feelings')
    connection.send_message(config.serialize())
    snapshot = cortex_pb2.Snapshot()
    snapshot.ParseFromString(connection.receive_message())
    return hello, snapshot


def run_server(host, port, publish, log=True):
    """
    Listen on host:port and pass received messages to publish

    Runs the server with the given address,
    using publish as callback giving it the received messages.

    example:
    >>> run_server('127.0.0.1', 8000, print)
    """
    with Listener(port, host) as listener:
        while True:
            client = listener.accept()
            threading.Thread(target=handle_connection, args=(client, publish, log)).start()


def publisher(publish):
    """Decorator"""
    def wrapper(*args, **kwargs):
        def bound(msg):
            return publish(msg, *args, **kwargs)
        return bound
    return wrapper


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
    #parse_translation(context, snapshot)
    #parse_color_image(context, snapshot)


def save_binary_data_to_filesystem(message, data_dir, lock=threading.Lock()):
    user_dir = data_dir / str(message[0].user_id)
    with lock:
        user_dir.mkdir(exist_ok=True)
    color = user_dir / (str(message[1].datetime) + '_color')
    color.write_bytes(message[1].color_image.data)
    depth = user_dir / (str(message[1].datetime) + '_depth')
    data = message[1].depth_image.data
    depth.write_bytes(struct.pack('%sf' % len(data), *data))
    return str(color.absolute()), str(depth.absolute())


@publisher
def publish_to_queue(message, host, port, data_dir):
    paths = save_binary_data_to_filesystem(message, data_dir)
    message = build_message(message, *paths)
    queue.publish(host, port, 'root', message, 'fanout')


def build_message(message, color_path, depth_path):
    return json.dumps({"user": {"id": message[0].user_id, "name": message[0].username,
                                "birthday": message[0].birthdate, "gender": message[0].gender},
                       "snapshot": {"timestamp": message[1].datetime,
                                    "translation": (message[1].pose.translation.x, message[1].pose.translation.y,
                                                    message[1].pose.translation.z),
                                    "rotation": (message[1].pose.rotation.x, message[1].pose.rotation.y,
                                                 message[1].pose.rotation.z, message[1].pose.rotation.w),
                                    "color": (message[1].color_image.width, message[1].color_image.height, color_path),
                                    "depth": (message[1].depth_image.width, message[1].depth_image.height, depth_path),
                                    "feelings": {"hunger": message[1].feelings.hunger,
                                                 "thirst": message[1].feelings.thirst,
                                                 "exhaustion": message[1].feelings.exhaustion,
                                                 "happiness": message[1].feelings.happiness}}})


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='localhost', show_default=True)
@click.option('-p', '--port', type=click.IntRange(0, 0xffff), default=8000, show_default=True, help="Port to listen on")
@click.option('-d', '--data-dir', type=click.Path(file_okay=False), default="data_dir/", help="Path to directory to "
                                                                                              "store binary data of "
                                                                                              "snapshots")
@click.option('--log/--no-log', default=True)
@click.argument('url')
def server(host, port, data_dir, log, url):
    """Runs the server listening on the given host and port or defaults to localhost:8000 if not provided
    Publishes the data given to a message queue with url from the argument url.
    Example for url is 'rabbitmq://localhost:5672'."""
    with net.SafetyNet():
        data_dir = pathlib.Path(data_dir)
        o = urlparse(url, scheme="rabbitmq")
        if o.scheme == 'rabbitmq':
            data_dir.mkdir(exist_ok=True)
            run_server(host, port, publish_to_queue(o.hostname, o.port, data_dir), log)
        else:
            # Scheme not supported
            raise click.UsageError('Unsupported Scheme for the queue url')


if __name__ == '__main__':
    cli(prog_name="python -m ducc.server")
