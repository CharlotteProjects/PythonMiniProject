#!/usr/bin/python

import MyColor

# ST7735 library
import digitalio, board
import adafruit_rgb_display.st7735 as st7735

# Drawing library
from PIL import Image, ImageDraw, ImageFont

# Font
font_0 = ImageFont.truetype("/user/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 12)
font_1 = ImageFont.truetype('Cretino.TTF', 12)
font_2 = ImageFont.truetype('AceRecords.ttf',12)

def init_ST7735():
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = digitalio.DigitalInOut(board.D24)

    BAUDRATE = 24000000 #24MHz

    spi = board.SPI()
    
    disp = st7735.ST7735R(
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE
    )
    return disp



# Display DHT11
def DisplayDHT11(disp, humidity, temperature):
    
    global font_0
    font = font_0
    
    BORDER = 2
    
    if disp.rotation % 180 == 90:
        height = disp.width
        width = disp.height
    else:
        width = disp.width
        height = disp.height

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle((0, 0, width, height), outline = MyColor.Color("BLACK"), fill = MyColor.Color("BLACK"))
    draw.rectangle((BORDER, BORDER, width-BORDER, height-BORDER-1), outline = MyColor.Color("WHITE"), fill = MyColor.Color("WHITE"))
    
    text_temp = ("Temperature: %d C" % temperature)
    text_humi = ("Humidity: %d %%" % humidity)
    
    (font_width, font_height) = font.getsize(text_temp)
    draw.text(
        (width // 2 - font_width // 2, height // 4 - font_height // 2),
        text_temp,
        font=font_0,
        fill=MyColor.Color("BLACK"),
    )
    
    (font_width, font_height) = font.getsize(text_humi)
    draw.text(
        (width // 2 - font_width // 2, height // 2 - font_height // 2),
        text_humi,
        font=font_0,
        fill=MyColor.Color("BLACK"),
    )
    
    disp.image(img)   
    #print("print Temperature completed")



def ImageProcess():
    (w, h) = img.size
    for i in range(0, w-1):
        for j in range(0, h-1):
            (r,g,b) = img.getpixel((i, j))
            img.putpixel((i, j), (b, g, r))