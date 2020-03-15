import json
from .api import parser


@parser('feelings')
def parse_feelings(data):
    d = json.loads(data)
    return json.dumps({"user": d["user"], "timestamp": d["snapshot"]["timestamp"],
                       "feelings": d["snapshot"]["feelings"]})
