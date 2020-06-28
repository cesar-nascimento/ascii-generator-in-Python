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


my_image = AsciiImage('example.jpg', 200, 0, Image.LANCZOS, color_dict.values())

if os.name == 'nt':
    os.system(f'mode con:cols={my_image.columns} lines={my_image.lines}')
    os.system('cls')
else:
    os.system(f'stty columns {my_image.columns}')
    os.system('clear')

print(my_image.ascii_string)
os.system('PAUSE')
