from io import BytesIO

from ducc import reader


def test_messages():
    lens = tuple(range(1, 5))
    f = BytesIO(b''.join((int.to_bytes(i, 4, 'little', signed=False) + bytes(i)) for i in lens))
    assert tuple(map(len, reader.messages(f))) == lens
