import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import ascii_generator
import palette_generator

window = tk.Tk()

var_path = tk.StringVar(value='example.jpg')
var_width = tk.IntVar(value=100)
var_dithering = tk.IntVar(value=0)

color_dict = {
        0: [[255, 0, 0], '\033[91m'],
        1: [[0, 255, 0], '\033[92m'],
        2: [[255, 255, 0], '\033[93m'],
        3: [[0, 0, 255], '\033[94m'],
        4: [[255, 0, 255], '\033[95m'],
        5: [[0, 255, 255], '\033[96m'],
        6: [[255, 255, 255], '\033[97m'],
        7: [[0, 0, 0], ' ']
    }

# Settings shortcuts
button_settings = {'bg': '#262626',
                   'fg': 'white',
                   'activebackground': 'white',
                   'activeforeground': '#262626',
                   'selectcolor': '#595959'}

color_config = {'foreground': 'white',
                'background': '#262626'}

window.title("ASCII Generator")
window.rowconfigure([0, 1], weight=0, pad=3)
window.columnconfigure([0, 1], weight=1, pad=3)
window.config(background='#262626')


frame_file_path = tk.Frame(master=window, bg='#262626')
frame_left = tk.Frame(master=window, bg='#262626')
frame_right = tk.Frame(master=window, bg='#262626')


# Labels
label_file_path = tk.Label(master=frame_file_path, text='File Path: ', **color_config)
label_file_path.pack(side=tk.LEFT, fill=tk.X)


label_width = tk.Label(master=frame_left, text='Width: ', **color_config)
label_width.grid(row=0, column=0, sticky='w')


label_choose_color = tk.Label(master=frame_left, text='Character color output:', **color_config)
label_choose_color.grid(row=3, column=0, columnspan=2, sticky='w')


# Entries
entry_file_path = tk.Entry(master=frame_file_path, width=100, textvariable=var_path)
entry_file_path.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)


ent_width = tk.Entry(master=frame_left, width=10, textvariable=var_width)
ent_width.grid(row=0, column=1, sticky='w')


# Buttons

def open_file():
    path = filedialog.askopenfilename()
    entry_file_path.delete(0, 'end')
    entry_file_path.insert(0, path)
    var_path.set(path)


button_file_path = tk.Button(master=frame_file_path, relief='flat', borderwidth=2,
                             text=' … ', **color_config, command=open_file)
button_file_path.pack(side=tk.RIGHT)


def unflat(original):
    factor = (original.width / 600)
    final_height = int((original.height / factor * 2))
    final = original.resize((600, final_height), resample=Image.LANCZOS)
    return final


def preview():
    global img_preview
    global img_output
    global canv_img
    black = [[0, 0, 0], ' ']
    colors = [var_red.get(), var_green.get(), var_yellow.get(), var_blue.get(),
              var_magenta.get(), var_cyan.get(), var_white.get(), black]

    color_list = [color_dict[i] for i in range(len(colors)) if colors[i] != 0]

    quantized_pal, mapp = palette_generator.generate_palette(*color_list)
    my_preview, img_output = ascii_generator.main(var_path.get(), var_width.get(), var_dithering.get(),
                                                  quantized_pal, mapp, resampling_options[f'{var_resample.get()}'])

    my_preview = unflat(my_preview)

    canv_img = ImageTk.PhotoImage(my_preview)
    canvas_preview.itemconfig(image_on_canvas, image=canv_img)


button_preview = tk.Button(master=frame_left, width=25, text='Preview', **color_config, command=preview)
button_preview.grid(row=10, column=0, columnspan=2, sticky='w')


def execute():
    preview()
    ascii_generator.print_ascii(img_output)


button_execute = tk.Button(master=frame_left, width=25, text='Generate ASCII Image', **color_config,
                           command=execute)
button_execute.grid(row=11, column=0, columnspan=2, sticky='w')


# Checkboxes
ch_dither = tk.Checkbutton(master=frame_left, text="Dithering", variable=var_dithering, **button_settings)
ch_dither.grid(row=1, column=0, columnspan=2, sticky='w')

var_red = tk.IntVar(value=1)
ch_red = tk.Checkbutton(master=frame_left, text="Red", variable=var_red, **button_settings,
                        command=None)
ch_red.grid(row=4, column=0, sticky='w')

var_green = tk.IntVar(value=1)
ch_green = tk.Checkbutton(master=frame_left, text="Green", variable=var_green, **button_settings,
                          command=None)
ch_green.grid(row=4, column=1, sticky='w')

var_yellow = tk.IntVar(value=1)
ch_yellow = tk.Checkbutton(master=frame_left, text="Yellow", variable=var_yellow, **button_settings,
                           command=None)
ch_yellow.grid(row=5, column=0, sticky='w')

var_blue = tk.IntVar(value=1)
ch_blue = tk.Checkbutton(master=frame_left, text="Blue", variable=var_blue, **button_settings,
                         command=None)
ch_blue.grid(row=5, column=1, sticky='w')

var_magenta = tk.IntVar(value=1)
ch_magenta = tk.Checkbutton(master=frame_left, text="Magenta", variable=var_magenta, **button_settings,
                            command=None)
ch_magenta.grid(row=6, column=0, sticky='w')

var_cyan = tk.IntVar(value=1)
ch_cyan = tk.Checkbutton(master=frame_left, text="Cyan", variable=var_cyan, **button_settings,
                         command=None)
ch_cyan.grid(row=6, column=1, sticky='w')

var_white = tk.IntVar(value=1)
ch_white = tk.Checkbutton(master=frame_left, text="White", variable=var_white, **button_settings,
                          command=None)
ch_white.grid(row=7, column=0, sticky='w')


# Right Box
quantized_palette, mapping = palette_generator.generate_palette(*color_dict.values())
img_preview, img_output = ascii_generator.main(var_path.get(), var_width.get(), var_dithering.get(),
                                               quantized_palette, mapping)

img_preview = unflat(img_preview)

canvas_preview = tk.Canvas(master=frame_right, width=600, height=600)
canvas_preview.pack(expand=1, fill='both')


canv_img = ImageTk.PhotoImage(img_preview)

image_on_canvas = canvas_preview.create_image(300, 300, image=canv_img)


# Option Menu
resampling_options = {'Lanczos': Image.LANCZOS, 'Nearest Neighbor': Image.NEAREST}
var_resample = tk.StringVar(value='Lanczos')
menu = tk.OptionMenu(frame_left, var_resample, *resampling_options.keys())
menu.config(width=23, **color_config, relief=tk.FLAT)
menu.grid(row=9, column=0, columnspan=2)


# Execute

frame_file_path.grid(row=0, column=0, columnspan=2, sticky='nwe')
frame_left.grid(row=1, column=0, sticky='nws')
frame_right.grid(row=1, column=1, sticky='ns')
window.mainloop()
