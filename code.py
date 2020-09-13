"""
Sending data to Adafruit IO and receiving it.
"""
import time
import board
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_button import Button
import adafruit_touchscreen
from digitalio import DigitalInOut
import busio
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
from adafruit_pyportal import PyPortal

# Import Adafruit IO HTTP Client
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# ESP32 SPI
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

'''
# ESP32 Setup
try:
    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)
except AttributeError:
    esp32_cs = DigitalInOut(board.D9)
    esp32_ready = DigitalInOut(board.D10)
    esp32_reset = DigitalInOut(board.D5)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
)  # Uncomment for Most Boards

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
'''
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Create an instance of the Adafruit IO HTTP client
io = IO_HTTP(aio_username, aio_key, wifi)

'''
try:
    # Get the 'temperature' feed from Adafruit IO
    #temperature_feed = io.get_feed("temperature")
    light_position_feed = io.get_feed("tiki-light-position")
except AdafruitIO_RequestError:
    # If no 'temperature' feed exists, create one
    #temperature_feed = io.create_new_feed("temperature")
    light_position_feed = io.create_new_feed("tiki-light-position")
'''

#######################
# For the feed 'tiki_light_position',
# value of 0 = lights are off
# value of 1 = lights are on
#######################

light_value = 1
light_position_feed = io.get_feed("tiki-light-position")

# Send random integer values to the feed
#random_value = randint(0, 50)
#print("Sending {0} to temperature feed...".format(random_value))
#io.send_data(temperature_feed["key"], random_value)
#io.send_data(light_position_feed["key"],25)
#print("Data sent!")


# Retrieve data value from the feed
#print("Retrieving data from tiki_light_position feed...")
#received_data = io.receive_data(light_position_feed["key"])
#print("Data from tiki_light_position feed: ", received_data["value"])


######################
# Create buttons
######################
# Initialize PyPortal Display
display = board.DISPLAY

WIDTH = board.DISPLAY.width  # 320
HEIGHT = board.DISPLAY.height  # 240

# Define basic display groups
splash = displayio.Group(max_size=10) # The Main Display Group

# Make the display context
button_group = displayio.Group(max_size=20)

# preload the font
print('loading font...')
font = bitmap_font.load_font("/fonts/Arial-ItalicMT-17.bdf")
#font = bitmap_font.load_font("/fonts/Arial-Bold-24.bdf")
#glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '
#font.load_glyphs(glyphs)

# button properties
print("creating buttons")
red = (255,0,0)
green = (50,205,50)
default_button_label = "Turn on/off lights"
buttons = []
button = Button(x=10, y=10, width=WIDTH-10, height=120,
                style=Button.SHADOWROUNDRECT,
                fill_color=green,
                outline_color=0x222222,
                name='test',
                label_font = font,
                label=default_button_label,
                )

buttons.append(button)
button_group.append(button.group)
splash.append(button_group)
#display.show(button_group)

print("creating touch screen object")
screen_width = WIDTH
screen_height = HEIGHT
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(screen_width, screen_height))

print("Drawing splash group to screen")
board.DISPLAY.show(splash)

print("starting forever touch loop")
while True:
    touched = ts.touch_point
    if touched:
        for button in buttons:
            if button.contains(touched):
                print("Touched", button.name)
                print("data", button.name)
                button.label = "PROCESSING"
                #button.fill_color = red
                io.send_data(light_position_feed["key"],25)
                button.label = default_button_label
                #button.fill_color = green
        time.sleep(0.05)