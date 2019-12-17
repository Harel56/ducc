import struct, datetime
class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id, self.timestamp, self.thought = user_id, timestamp, thought
    def __repr__(self):
        return f'Thought(user_id={self.user_id}, timestamp={self.timestamp!r}, thought={self.thought!r})'
    def __str__(self):
        return '[%04d-%02d-%02d %02d:%02d:%02d] user %d: %s' % (self.timestamp.year, self.timestamp.month, self.timestamp.day, self.timestamp.hour, self.timestamp.minute, self.timestamp.second, self.user_id, self.thought)
    def __eq__(self, other):
        return isinstance(other, Thought) and (self.user_id, self.timestamp, self.thought) == (other.user_id, other.timestamp, other.thought)
    def serialize(self):
        msg = self.thought.encode()
        return struct.pack('QQI',  self.user_id, int(self.timestamp.timestamp()), len(msg)) + msg
    def deserialize(data):
        info = struct.unpack('QQI', data[:20])
        return Thought(info[0], datetime.datetime.fromtimestamp(info[1]), data[20:].decode())

