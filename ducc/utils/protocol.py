import datetime
import struct


class Hello:
    def __init__(self, user_id, username, birthdate, gender):
        self.user_id = user_id
        self.username = username
        self.birthdate = birthdate
        self.gender = gender

    def __eq__(self, other):
        if not isinstance(other, Hello):
            return NotImplemented
        return self.user_id == other.user_id and self.username == other.user_id \
            and self.birthdate == other.birthdate and self.gender == other.gender

    def serialize(self):
        encoded_name = self.username.encode()
        return struct.pack('QI', self.user_id, len(encoded_name)) + encoded_name + struct.pack('Ic', self.birthdate,
                                                                                               self.gender.encode())

    @classmethod
    def deserialize(cls, data):
        user_id, name_length = struct.unpack('QI', data[:12])
        username = data[12:12 + name_length].decode()
        birthdate, gender = struct.unpack('Ic', data[12 + name_length:17 + name_length])
        return cls(user_id, username, birthdate, gender.decode())


class Config:
    def __init__(self, *fields):
        self.fields = fields

    def __len__(self):
        return len(self.fields)

    def encode_fields(self):
        for field in self.fields:
            data = field.encode()
            yield struct.pack('I', len(data)) + data

    def serialize(self):
        return struct.pack('I', len(self)) + b''.join(self.encode_fields())

    @classmethod
    def deserialize(cls, data):
        return cls(*decode_fields(data[4:]))


def decode_fields(data):
    position = 0
    while position < len(data):
        length, = struct.unpack('I', data[position:position + 4])
        position += 4
        yield data[position:position + length].decode()
        position += length


class Feelings:
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

    def __repr__(self):
        return f'Feelings({self.hunger!r}, {self.thirst!r}, {self.exhaustion!r}, {self.happiness!r})'

    def __eq__(self, other):
        if not isinstance(other, Feelings):
            return NotImplemented
        return self.hunger == other.hunger and self.thirst == other.thirst and self.exhaustion == other.exhaustion and self.happiness == other.happiness

    def __hash__(self):
        return hash(tuple(self))

    def __iter__(self):
        return iter((self.hunger, self.thirst, self.exhaustion, self.happiness))


class Snapshot:
    def __init__(self, timestamp, color, depth, translation=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0, 0.0), hunger=0.0,
                 thirst=0.0, exhaustion=0.0, happiness=0.0):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color = color
        self.depth = depth
        self.feelings = Feelings(hunger, thirst, exhaustion, happiness)

    def datetime(self):
        return datetime.datetime.fromtimestamp(self.timestamp / 1000)

    def serialize(self):
        return struct.pack('QdddddddII', self.timestamp, *self.translation, *self.rotation, *self.color[:2]) + \
               self.color[2] + struct.pack('II', *self.depth[:2]) + self.depth[2] + struct.pack('ffff', *self.feelings)

    @classmethod
    def deserialize(cls, data):
        timestamp, tx, ty, tz, rx, ry, rz, rw, h, w = struct.unpack('QdddddddII', data[:72])
        location = 72 + 3 * w * h
        color = w, h, data[72:location]
        location2 = 8 + location
        h, w = struct.unpack('II', data[location:location2])
        location = 4 * w * h + location2
        depth = w, h, data[location2:location]
        feelings = struct.unpack('ffff', data[location:location + 16])
        return cls(timestamp, color, depth, (tx, ty, tz), (rx, ry, rz, rw), *feelings)
