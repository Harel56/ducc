import pathlib
import threading
from .utils import Listener, Hello, Config, Snapshot
from .parsers import parse_translation, parse_color_image


class Context:
    def __init__(self, root, lock):
        self.root = root
        self.lock = lock

    def path(self, file_name):
        return self.root / file_name

    def save(self, file_name, data):
        with self.lock:
            with self.path(file_name).open('w') as f:
                f.write(data)


def handle_connection(connection, data_dir, lock=threading.Lock()):
    data_dir = pathlib.Path(data_dir)
    with connection:
        hello = Hello.deserialize(connection.receive_message())
        config = Config('translation', 'color_image')
        connection.send_message(config.serialize())
        snapshot = Snapshot.deserialize(connection.receive_message())
    dt = snapshot.datetime()
    user_dir = data_dir / str(hello.user_id)
    dir_path = user_dir / ("%04d-%02d-%02d_%02d-%02d-%02d-%06d" % (
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond))
    with lock:
        user_dir.mkdir(exist_ok=True)
        dir_path.mkdir(exist_ok=True)
    context = Context(dir_path, lock)
    parse_translation(context, snapshot)
    parse_color_image(context, snapshot)


def run_server(address, data_dir):
    """
    Runs the server with the given address,
    using directory with path given by argument data_dir.

    example:
    >>> run_server(('127.0.0.1', 8000), 'data/')
    """
    listener = Listener(address[1], address[0])
    listener.start()
    while True:
        client = listener.accept()
        threading.Thread(target=handle_connection, args=(client, data_dir)).start()


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        address = argv[1].split(':', 1)
        address[1] = int(address[1])
        run_server(tuple(address), argv[2])
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
