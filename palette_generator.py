from PIL import Image
import numpy as np


# From boldest to palest
graded_chars = ['@', '%', '#', '*', '+', '=', '-', ':', '.']
grad_range = len(graded_chars)


def make_rgb_palette(colors):
    # Generate an RGB palette
    my_palette = np.zeros(shape=[1, 768], dtype=np.uint8)

    for x in range(len(colors)):
        color = colors[x][0]
        step = 128 // grad_range
        descend = [255 - i * step for i in range(grad_range)]
        ascend = [0 + i * step for i in range(grad_range)]

        if color == [0, 0, 0]:
            continue

        if color == [255, 255, 255]:
            step = 256 // grad_range
            descend = [255 - i * step for i in range(grad_range)]

        for i in range(3):
            index = x * grad_range * 3 + i
            value = color[i]
            if value == 255:
                my_palette[0, index: index + 3 * grad_range: 3] = descend
            elif value == 0:
                my_palette[0, index: index + 3 * grad_range: 3] = ascend
            else:
                raise Exception('Input RGB values must be either 255 or 0')
    return my_palette


def make_char_palette(colors):
    # uses the same range of 768 as the rgb palette, ' ' is empty and will be mapped to the black color
    my_palette = np.array([' ' for _ in range(768)], dtype='O')

    for x in range(len(colors)):
        color = colors[x][1]
        if color == ' ':
            continue
        else:
            char_grad = np.array([color + char for char in graded_chars], dtype=my_palette.dtype)
            index = x * grad_range
            my_palette[index: index + grad_range] = char_grad

    return my_palette


def generate_palette(*color_list):

    rgb_palette = make_rgb_palette(color_list)

    palette_image = Image.new('P', (1, 1))  # the palette must be associated with an image
    palette_image.putpalette(rgb_palette)

    char_palette = make_char_palette(color_list)

    return palette_image, char_palette
