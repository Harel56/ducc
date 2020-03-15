import json
from .api import parser


@parser('pose')
def parse_pose(data):
    d = json.loads(data)
    return json.dumps({"user": d["user"], "timestamp": d["snapshot"]["timestamp"],
                       "pose": {"translation": d["snapshot"]["translation"], "rotation": d["snapshot"]["rotation"]}})


# parse_pose.field = 'pose'
