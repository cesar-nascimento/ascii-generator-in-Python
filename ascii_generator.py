from PIL import Image
import numpy as np
import os
import palette_generator


def resize(original: Image.Image, final_width=25, resample=Image.LANCZOS):
    # Each character is roughly 8 pixels wide and 16 pixels tall.
    # We squish the picture a little to counter that.
    factor = original.width / final_width
    final_height = int((original.height / factor) / 2)
    final = original.resize((final_width, final_height), resample=resample)
    return final


def print_ascii(output):
    os.system('@echo off')
    os.system('cls')
    lines, cols = output.shape
    os.system(f'mode con:cols={cols} lines={lines}')
    final = '\n'.join(''.join(char for char in row.flat) for row in output)
    print(final)


def main(path, width, dither, pal_image, char_pal, resample_method=Image.LANCZOS):
    my_image = Image.open(path)

    small_image = resize(my_image, width, resample_method)
    small_image_rgb = small_image.convert(mode='RGB')

    quantized_small_image = small_image_rgb.quantize(dither=dither, palette=pal_image)
    data = np.asarray(quantized_small_image)

    output = char_pal[data]
    # 'output' is like an image where each pixel is replaced with a character.
    return quantized_small_image, output


if __name__ == '__main__':

    color_dict = {
        'red': [[255, 0, 0], '\033[91m'],
        'green': [[0, 255, 0], '\033[92m'],
        'yellow': [[255, 255, 0], '\033[93m'],
        'blue': [[0, 0, 255], '\033[94m'],
        'magenta': [[255, 0, 255], '\033[95m'],
        'cyan': [[0, 255, 255], '\033[96m'],
        'white': [[255, 255, 255], '\033[97m'],
        'black': [[0, 0, 0], ' ']
    }

    palette_image, char_palette = palette_generator.generate_palette(*color_dict.values())
    file_path = 'example.jpg'
    width_resolution = 600
    dithering = 0
    img_preview, img_output = main(file_path, width_resolution, dithering, palette_image, char_palette)
    print_ascii(img_output)
    os.system('PAUSE')
