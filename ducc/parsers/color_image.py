import json
from PIL import Image
from .api import parser


IMAGE_FORMAT = '.jpg'


@parser('color')
def parse_color_image(data):
    d = json.loads(data)
    with open(d["snapshot"]["color"][2], 'rb') as fp:
        img_data = fp.read()
    image = Image.frombytes('RGB', d["snapshot"]["color"][:2], img_data)
    d["snapshot"]["color"][2] += IMAGE_FORMAT
    image.save(d["snapshot"]["color"][2])
    return json.dumps({"user": d["user"], "timestamp": d["snapshot"]["timestamp"],
                       "color": (d["snapshot"]["color"][2])})
