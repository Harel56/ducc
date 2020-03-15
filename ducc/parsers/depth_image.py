import json
import matplotlib.pyplot as plt
import numpy as np
import struct
from .api import parser


IMAGE_FORMAT = '.png'


@parser('depth')
def parse_depth_image(data):
    d = json.loads(data)
    with open(d["snapshot"]["depth"][2], 'rb') as fp:
        img_data = fp.read()
    mat = np.array(struct.unpack('%sf' % (d["snapshot"]["depth"][0] * d["snapshot"]["depth"][1]), img_data)).\
        reshape((d["snapshot"]["depth"][1]))
    d["snapshot"]["depth"][2] += IMAGE_FORMAT
    plt.imshow(mat)
    plt.savefig(d["snapshot"]["depth"][2])
    return json.dumps({"user": d["user"], "timestamp": d["snapshot"]["timestamp"], "depth": d["snapshot"]["depth"]})
