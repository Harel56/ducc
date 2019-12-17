import datetime
import struct


class Reader:
    def __repr__(self):
        return '<' + str(self) + '>'

    def __str__(self):
        return f"user {self.user_id}: {self.username}, born {datetime.date.fromtimestamp(self.birthdate).strftime('%B %d, %Y')} ({'male' if self.gender == 'm' else 'female' if self.gender == 'f' else 'other'})"

    def __iter__(self):
        return iter(self.snapshots)

    def __init__(self, f):
        uint = lambda size: int.from_bytes(f.read(size), 'little', signed=False)
        self.user_id = uint(8)
        self.username = f.read(uint(4)).decode()
        self.birthdate = uint(4)
        self.gender = f.read(1).decode()
        self.snapshots = parse_snapshots(f)

    @classmethod
    def from_path(cls, path):
        cls(open(path, 'rb'))


class Snapshot:
    def __init__(self, timestamp, translation, rotation, color, depth, hunger, thirst, exhaustion, happiness):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color = color
        self.depth = depth
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

    def __repr__(self):
        return '<' + str(self) + '>'

    def __str__(self):
        return f"Snapshot from {datetime.datetime.fromtimestamp(self.timestamp / 1000)} on {self.translation} / " + \
               f"{self.rotation} with a {self.color[:2]} color image and a {self.depth[:2]} depth image."

    @classmethod
    def parse_snapshot(cls, f):
        """Parse one snapshot from the given file descriptor.
        returns a Snapshot object."""
        timestamp, tx, ty, tz, rx, ry, rz, rw, h, w = struct.unpack('QdddddddII', f.read(72))
        color = (w, h, f.read(3 * w * h))
        h, w = struct.unpack('II', f.read(8))
        depth = (w, h, f.read(4 * w * h))
        feelings = struct.unpack('ffff', f.read(16))
        return cls(timestamp, (tx, ty, tz), (rx, ry, rz, rw), color, depth, *feelings)


def parse_snapshots(f):
    """Generator for snapshots.
    argument f should be a file stream"""
    try:
        while True:
            yield Snapshot.parse_snapshot(f)
    except struct.error:  # Snapshot.parse_snapshot raises struct.error upon reaching EOF
        f.close()
