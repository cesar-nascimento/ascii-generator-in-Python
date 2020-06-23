from PIL import Image
import numpy as np


class AsciiImage:

    def __init__(self, path, final_width, dithering, resample, *colors):
        self.image = Image.open(path)
        self.colors = list(*colors)
        self.final_width = int(final_width)
        self.dithering = int(dithering)
        self.resample = resample
        self.graded_chars = """@%#*+=-:."""
        self.lines = self.resized.height
        self.columns = self.resized.width

    @property
    def resized(self):
        # Each character is roughly 8 pixels wide and 16 pixels tall.
        # We squish the picture a little to counter that.
        factor = self.image.width / self.final_width
        final_height = int((self.image.height / factor) / 2)
        resized = self.image.resize((self.final_width, final_height), resample=self.resample)
        return resized.convert(mode='RGB')

    @property
    def rgb_palette(self):
        # Generate an RGB palette with 768 fields
        my_palette = np.zeros(shape=[1, 768], dtype=np.uint8)

        grad_range = len(self.graded_chars)

        for x in range(len(self.colors)):
            color = self.colors[x].rgb
            step = 128 // grad_range
            descend = [255 - i * step for i in range(grad_range)]
            ascend = [0 + i * step for i in range(grad_range)]

            if color == (0, 0, 0):
                continue

            if color == (255, 255, 255):
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

    @property
    def char_palette(self):
        # uses the same range of 768 as the rgb palette, ' ' is empty therefore it will be mapped to the black color
        my_palette = np.array([' ' for _ in range(768)], dtype='O')

        grad_range = len(self.graded_chars)
        for x in range(len(self.colors)):
            color = self.colors[x].ansi_code
            if color == ' ':
                continue
            else:
                char_grad = np.array([color + char for char in self.graded_chars], dtype=my_palette.dtype)
                index = x * grad_range
                my_palette[index: index + grad_range] = char_grad

        return my_palette

    @property
    def palette_container(self):

        palette_image = Image.new('P', (1, 1))  # the palette must be associated with an image
        palette_image.putpalette(self.rgb_palette)

        return palette_image

    @property
    def ascii_string(self):
        data = np.asarray(self.resized_quantized)
        numpy_string = self.char_palette[data]
        return '\n'.join(''.join(char for char in row.flat) for row in numpy_string)

    @property
    def resized_quantized(self):
        return self.resized.quantize(dither=self.dithering, palette=self.palette_container)

    def get_preview(self, final_width=600):
        factor = (self.resized.width / final_width)
        final_height = int((self.resized.height / factor * 2))
        return self.resized_quantized.resize((final_width, final_height), resample=Image.NEAREST)


class Color:
    def __init__(self, rgb, ansi_code):
        self.rgb = tuple(rgb)
        self.ansi_code = str(ansi_code)
