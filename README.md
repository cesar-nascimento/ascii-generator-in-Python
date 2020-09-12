# ASCII-Generator-in-Python
An easy way to create colorful ASCII art directly on the console.

![Example](https://i.imgur.com/mon0pFv.png)

## Installation and usage

### Method 1 - cloning

Clone the repo, then cd into it's folder and run `pip install -r requirements.txt`.

This will install the following libraries:

  * [Numpy](https://pypi.org/project/numpy/)
  
  * [Pillow](https://pypi.org/project/Pillow/)

Run gui.py to launch the user interface.

### Method 2 - using docker

If you already familiar with docker, this method is probably the easiest.

Pull the docker image with `docker pull cesar0nascimento/ascii-generator-in-python`.

#### Windows: 
run with `docker run --rm -it -e DISPLAY=<host_ip>:0.0 -v <path_to_images>:/home cesar0nascimento/ascii-generator-in-python`.

you're also going to need to install [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/).

replace `<host_ip>` with your local ip address (run ipconfig to get that).

replace `<path_to_images>` with the **absolute path** to where the images you want to convert are located.

#### Linux
run with `docker run --rm -it -e DISPLAY=$DISPLAY -v <path_to_images>:/home cesar0nascimento/ascii-generator-in-python`.

replace `<path_to_images>` with the **absolute path** to where the images you want to convert are located.

## How to use
Run gui.py to launch the user interface.

**File Path:** Either paste the path to the image you want to convert to ASCII or use the button on the right to navigate and select an image.

**Width:** Width controls the maximum number of characters to be displayed on a line. if it's too low then the image probably won't look good, if it's too high you won't be able to see the full image unless you scale down the console. A number between 50 and 250 usually works well.

**Dithering:** Some images look better with dithering enabled while others will look awful.

**Character color output:** Select at least one color or any combination you want.

**Lanczos:** Better for photos and images with lots of details.

**Nearest Neighbor:** Better for pixelated images.

Hit Preview and then click Generate to print the ASCII image on the console.
