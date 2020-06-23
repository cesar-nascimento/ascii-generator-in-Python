from ascii import AsciiImage, Color
import os
from PIL import Image


color_dict = {
        'red': Color((255, 0, 0), '\033[91m'),
        'green': Color((0, 255, 0), '\033[92m'),
        'yellow': Color((255, 255, 0), '\033[93m'),
        'blue': Color((0, 0, 255), '\033[94m'),
        'magenta': Color((255, 0, 255), '\033[95m'),
        'cyan': Color((0, 255, 255), '\033[96m'),
        'white': Color((255, 255, 255), '\033[97m'),
        'black': Color((0, 0, 0), ' ')
    }


a = AsciiImage('example.jpg', 100, 0, Image.LANCZOS, color_dict.values())
a.get_preview(10).show()
b = a.ascii_string

os.system('@echo off')
os.system('cls')

os.system(f'mode con:cols={a.columns} lines={a.lines}')
print(b)

