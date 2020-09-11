import time
import board
import busio
import digitalio
import storage
import os
import displayio
from adafruit_bitmap_font import bitmap_font
import adafruit_sdcard
import audioio
from adafruit_pyportal import PyPortal
from adafruit_button import Button

# to read docs for PyPortal:
# https://github.com/adafruit/Adafruit_CircuitPython_PyPortal/blob/master/adafruit_pyportal.py#L255

# Set up where we'll be fetching data from
#DATA_SOURCE = "https://www.adafruit.com/api/quotes.php"
#QUOTE_LOCATION = [0, 'text']
#AUTHOR_LOCATION = [0, 'author']

# the current working directory (where this file is)
# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]
'''
pyportal = PyPortal(url= None,
                    json_path = None,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=cwd+"/quote_background.bmp",
                    text_font=cwd+"/fonts/Arial-ItalicMT-17.bdf",
                    text_position=((20, 120),  # quote location
                                   (5, 210)), # author location
                    text_color=(0xFFFFFF,  # quote text color
                                0x8080FF), # author text color
                    text_wrap=(35, # characters to wrap for quote
                               0), # no wrap for author
                    text_maxlen=(180, 30), # max text size for quote & author
                   )
'''
BACKGROUND_COLOR = 0x443355
pyportal = PyPortal(default_bg=BACKGROUND_COLOR)

# speed up projects with lots of text by preloading the font!
# pyportal.preload_font()

# Default location to look is in internal memory
MUSIC_DIRECTORY = "/sd/music"

######################
# Create buttons
######################
the_font = '/fonts/Arial-ItalicMT-17.bdf'
font = bitmap_font.load_font(the_font)
buttons = []
button = Button(x=10, y=10, width=120, height=60,
                style=Button.SHADOWROUNDRECT,
                fill_color=(255, 0, 0),
                outline_color=0x222222,
                name='test',
                label_font = font,
                label='Bad to the Bone',
                )
pyportal.splash.append(button.group)
buttons.append(button)
# Next button

while True:
    touched = pyportal.touchscreen.touch_point
    # Returns tuple of (X,Y,?)
    # X range 0...320
    # Y range 0...240
    if touched:
        for button in buttons:
            if button.contains(touched):
                print("Touched", button.name)
                print("data", button.name)


        time.sleep(0.3)