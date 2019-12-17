from datetime import datetime
from .reader import Reader
from .utils import Connection, Hello, Config, Snapshot


'''def upload_thought(address, user_id, thought):
    th = Thought(user_id, datetime.today(), thought)
    with Connection.connect(*address) as conn:
        conn.send(th.serialize())
'''


def run_client(address, sample):
    """
    Runs the client connecting to the address given by argument 'address',
    reading data from file given by sample

    example:
    >>>sample = open('sample.mind')
    >>>run_client(('127.0.0.1', 8000), sample)
    """
    reader = Reader(sample)
    for snapshot in reader:
        with Connection.connect(*address) as connection:
            hello_msg = Hello(reader.user_id, reader.username, reader.birthdate, reader.gender)
            connection.send_message(hello_msg.serialize())
            config_msg = Config.deserialize(connection.receive_message())
            optional = {'translation':snapshot.translation, 'rotation':snapshot.rotation, 'hunger':snapshot.hunger, 'thirst':snapshot.thirst, 'happiness':snapshot.happiness}
            snapshot_msg = Snapshot(snapshot.timestamp, snapshot.color, snapshot.depth,
                                    **{key: value for (key, value) in optional.items() if (key in config_msg.fields)})
            connection.send_message(snapshot_msg.serialize())


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <thought>')
        return 1
    try:
        address = argv[1].split(':', 1)
        address[1] = int(address[1])
        run_client(tuple(address), argv[2])
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
