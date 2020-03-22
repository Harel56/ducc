import datetime as dt
import json
import os
import time
import pytest

from ducc import parsers

_TIME = time.time() * 1000


@pytest.fixture
def message(tmp_path):
    (tmp_path / 'color_path').write_bytes(bytes(36))
    (tmp_path / 'depth_path').write_bytes(bytes(48))
    return json.dumps(
        {"user": {"id": 71, "name": "Harel Etgar", "birthday": dt.datetime(2001, 3, 29).timestamp(), "gender": 'm'},
         "snapshot": {"timestamp": _TIME, "translation": (1, 2, 3), "rotation": (5, 6, 7, 8),
                      "color": (3, 4, str(tmp_path / 'color_path')),
                      "depth": (3, 4, str(tmp_path / 'depth_path')),
                      "feelings": {"hunger": 0.0, "thirst": 0.0, "exhaustion": 0.0, "happiness": 0.0}}}), tmp_path


def test_pose(message):
    result = parsers.run_parser('pose', message[0])
    assert result == json.dumps(
        {"user": {"id": 71, "name": "Harel Etgar", "birthday": dt.datetime(2001, 3, 29).timestamp(), "gender": 'm'},
         "timestamp": _TIME, "pose": {"translation": (1, 2, 3), "rotation": (5, 6, 7, 8)}})


def test_feelings(message):
    result = parsers.run_parser('feelings', message[0])
    assert result == json.dumps(
        {"user": {"id": 71, "name": "Harel Etgar", "birthday": dt.datetime(2001, 3, 29).timestamp(), "gender": 'm'},
         "timestamp": _TIME, "feelings": {"hunger": 0.0, "thirst": 0.0, "exhaustion": 0.0, "happiness": 0.0}})


def test_color(message):
    result = parsers.run_parser('color', message[0])
    assert result == json.dumps(
        {"user": {"id": 71, "name": "Harel Etgar", "birthday": dt.datetime(2001, 3, 29).timestamp(), "gender": 'm'},
         "timestamp": _TIME, "color": (3, 4, str(message[1] / 'color_path.jpg'))})
    assert (message[1] / 'color_path.jpg').is_file()


def test_depth(message):
    result = parsers.run_parser('depth', message[0])
    assert result == json.dumps(
        {"user": {"id": 71, "name": "Harel Etgar", "birthday": dt.datetime(2001, 3, 29).timestamp(), "gender": 'm'},
         "timestamp": _TIME, "depth": (3, 4, str(message[1] / 'depth_path.png'))})
    assert (message[1] / 'depth_path.png').is_file()
