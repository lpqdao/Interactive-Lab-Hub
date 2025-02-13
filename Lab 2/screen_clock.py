import time
from datetime import datetime
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 

    now = datetime.now()
    now_str = now.strftime("%m/%d/%Y %H:%M:%S")

    winter = datetime(2021, 12, 1, 0, 0, 0)
    inter = winter - now

    spring = datetime(2022, 3, 23, 0, 0, 0)
    inter_spr = spring - now

    line1 = now_str
    line2 = "GOOD MORNING!!"
    line3 =  "We have " +str(inter.seconds)+ "seconds til "
    line4 = "winter to we celebrate"
    line5= "Christmas!!"
    line6 = "We have "  +str(inter_spr.seconds)+ "seconds til"
    line7 = "spring!!! WOOOO"
 
    y = top
    draw.text((x,y), line1, font=font, fill='#58815b')
    y += font.getsize(line1)[1]
    draw.text((x,y), line2, font=font, fill='#d1414a')
    y += font.getsize(line2)[1]
    draw.text((x,y), line3, font=font, fill='#5c76bc')
    y += font.getsize(line3)[1]
    draw.text((x,y), line4, font=font, fill='#5c74bc')
    y += font.getsize(line4)[1]
    draw.text((x,y), line5, font=font, fill='#5c74bc')
    y += font.getsize(line5)[1]
    draw.text((x,y), line6, font=font, fill='#FFFFFF')
    y += font.getsize(line6)[1]
    draw.text((x,y), line7, font=font, fill='#FFFFFF')
    y += font.getsize(line7)[1]
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)


