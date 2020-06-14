from PIL import Image
import numpy as np
from colorama import init
init()


# From boldest to palest
graded_chars = ['@', '%', '#', '*', '+', '=', '-', ':', '.']
grad_range = len(graded_chars)


def rgb_gradient(color):
    """Generate, RGB gradient list.
    Each color descends from 255 to almost 0."""
    grad = []
    for i in range(grad_range):

        r, g, b = 0, 0, 0
        if color[0] > 0:
            r = color[0] - i * (255 // grad_range)
        if color[1] > 0:
            g = color[1] - i * (255 // grad_range)
        if color[2] > 0:
            b = color[2] - i * (255 // grad_range)
        grad.append([r, g, b])
    return grad


def char_gradient(color):
    # We need a list of len(graded_chars) filled with empty ' ' for the black color.
    if color[3] == ' ':
        return list(' ' * grad_range)
    pixel_character_grad = []
    for char in graded_chars:
        pixel_character_grad.append(color[3] + char)
    return pixel_character_grad


def generate_palette(color_list):

    # Every color has a range equal to the number of chars on the list of ASCII characters.
    # Except for black, which is range 1, because it's empty -> (' ').
    # this calculates how many colors the final image will have.
    color_range = ((len(color_list) - 1) * grad_range) + 1

    color_matrix = list(map(rgb_gradient, color_list))
    color_array = np.array(color_matrix, dtype='uint8')

    char_matrix = list(map(char_gradient, color_list))
    char_array = np.array(char_matrix, dtype='unicode_')

    palette = Image.fromarray(color_array, mode='RGB')
    quantized_palette = palette.quantize(colors=color_range)

    numpy_array_palette = np.asarray(quantized_palette)

    mapping = np.zeros(numpy_array_palette.max()+1, dtype=char_array.dtype)

    # "mapping" is like a palette but instead of using color it uses
    # a combination of ANSI codes for each color combined with ASCII characters
    mapping[numpy_array_palette] = [char_array]
    return quantized_palette, mapping
