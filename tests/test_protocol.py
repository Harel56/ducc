import datetime as dt

from ducc.utils import protocol


def test_hello():
    hello = protocol.Hello(3, "Harel Etgar", int(dt.datetime(2001, 3, 29).timestamp()), 'm')
    assert protocol.Hello.deserialize(hello.serialize()) == hello


def test_config():
    config = protocol.Config("hello", "world")
    assert protocol.Config.deserialize(config.serialize()) == config


def test_snapshot():
    pass
