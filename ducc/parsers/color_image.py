from PIL import Image


def parse_color_image(context, snapshot):
    image = Image.frombytes('RGB', (snapshot.color[0], snapshot.color[1]), snapshot.color[2])
    image.save(context.path('color_image.jpg'))
