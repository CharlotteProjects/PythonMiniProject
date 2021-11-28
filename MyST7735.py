#!/usr/bin/python

import MyColor
import time

# ST7735 library
import digitalio, board
import adafruit_rgb_display.st7735 as st7735

# Drawing library
from PIL import Image, ImageDraw, ImageFont

# Font
font_0 = ImageFont.truetype("DejaVuSans.ttf", 12)
# login Title
font_1 = ImageFont.truetype('AntiqueQuestSt.ttf',16)
# Member Name
font_2 = ImageFont.truetype('DevinneSwash.ttf',14)
font_2a = ImageFont.truetype('DevinneSwash.ttf',11)

font_3 = ImageFont.truetype('Cretino.TTF', 12)
font_4 = ImageFont.truetype('AceRecords.ttf',12)

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
        rotation=270,
        baudrate=BAUDRATE,
        x_offset = 2,
        y_offset = 2,
    )
    return disp


# Display Login
def DisplayLogin(disp):
    
    global font_1
    global font_2
    global font_2a
    font = font_1
    
    if disp.rotation % 180 == 90:
        height = disp.width
        width = disp.height
    else:
        width = disp.width
        height = disp.height

    text_1 = "Smart"
    text_2 = "Security"
    text_3 = "System"
    
    color = 255
    hide = False
    pass_1 = False

    while not pass_1:
        
        if hide == False:
            color = color - 10
        else:
            color = color + 10

        # it will stay 3 second
        if color < 0:
            hide = True
            color = 0
            time.sleep(2.5)
        
        if color > 255:
            color = 255
            pass_1 = True
    
        img = Image.open("background.jpg")
        img = img.resize((width, height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(img)
        
        (font_width, font_height) = font.getsize(text_1)
        draw.text(
            (width // 2 - font_width // 2, height // 2 - font_height // 2 - 26),
            text_1,
            font = font_1,
            fill=(color, color, color)
        )
    
        (font_width, font_height) = font.getsize(text_2)
        draw.text(
            (width // 2 - font_width // 2, height // 2 - font_height // 2),
            text_2,
            font = font_1,
            fill=(color, color, color)
        )
        
        (font_width, font_height) = font.getsize(text_3)
        draw.text(
            (width // 2 - font_width // 2, height // 2 - font_height // 2 +26),
            text_3,
            font = font_1,
            fill=(color, color, color)
        )
        disp.image(img)
        time.sleep(0.06)
    
# Display Name
    
    text_4 = "Member"
    text_5 = "Kwok Kei"
    text_6 = "200324199"
    text_7 = "Cheng Kwok Leung"
    text_8 = "200304465"
    text_9 = "Chan Ka Ho"
    text_10 = "200234201"
    
    color = 255
    hide = False
    pass_1 = False
    
    while not pass_1:
        
        if hide == False:
            color = color - 10
        else:
            color = color + 10

        # it will stay 4 second
        if color < 0:
            hide = True
            color = 0
            time.sleep(4)
        
        if color > 255:
            color = 255
            pass_1 = True
    
        img = Image.open("background.jpg")
        img = img.resize((width, height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(img)
        
        # Text : Member
        (font_width, font_height) = font.getsize(text_4)
        draw.text(
            (width // 2 - font_width // 2, 0),
            text_4,
            font = font_1,
            fill=(color, color, color)
        )
        
        # Text : Kwok Kei
        (font_width, font_height) = font.getsize(text_5)
        draw.text(
            (4, 30),
            text_5,
            font = font_2,
            fill=(color, color, color)
        )
        
        (font_width, font_height) = font.getsize(text_6)
        draw.text(
            (4, 46),
            text_6,
            font = font_2,
            fill=(color, color, color)
        )
        
        # Text : Cheng Kwok Leung
        (font_width, font_height) = font.getsize(text_7)
        draw.text(
            (4, 60),
            text_7,
            font = font_2a,
            fill=(color, color, color)
        )
        
        (font_width, font_height) = font.getsize(text_8)
        draw.text(
            (4, 76),
            text_8,
            font = font_2,
            fill=(color, color, color)
        )
        
        # Text : Chan Ka Ho
        (font_width, font_height) = font.getsize(text_9)
        draw.text(
            (4, 90),
            text_9,
            font = font_2,
            fill=(color, color, color)
        )
        
        (font_width, font_height) = font.getsize(text_10)
        draw.text(
            (4, 106),
            text_10,
            font = font_2,
            fill=(color, color, color)
        )
        
        disp.image(img)
        time.sleep(0.06)


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

    # White backgound
    #img = Image.new("RGB", (width, height))
    # My Background
    img = Image.open("background.jpg")
    img = img.resize((width, height), Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)
    
    #draw.rectangle((0, 0, width, height), outline = MyColor.Color("BLACK"), fill = MyColor.Color("BLACK"))
    #draw.rectangle((BORDER, BORDER, width-BORDER, height-BORDER-1), outline = MyColor.Color("WHITE"), fill = MyColor.Color("WHITE"))
    
    text_temp = ("Temperature: %d C" % temperature)
    text_humi = ("Humidity: %d %%" % humidity)
    
    (font_width, font_height) = font.getsize(text_temp)
    draw.text(
        (width // 2 - font_width // 2, height // 4 - font_height // 2),
        text_temp,
        font = font_0,
        fill=MyColor.Color("BLACK"),
    )
    
    (font_width, font_height) = font.getsize(text_humi)
    draw.text(
        (width // 2 - font_width // 2, height // 2 - font_height // 2),
        text_humi,
        font = font_0,
        fill=MyColor.Color("BLACK"),
    )
    
    disp.image(img)   
    #print("print Temperature completed")

def DisplayCamera(disp, img):
    global font_1
    font = font_1
    
    if disp.rotation % 180 == 90:
        height = disp.width
        width = disp.height
    else:
        width = disp.width
        height = disp.height
    
    if img is not None:
        img = img.resize((width, height), Image.ANTIALIAS)
    else:
        img = Image.open("background.jpg")
        img = img.resize((width, height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(img)
        (font_width, font_height) = font.getsize(text_temp)
        draw.text(
            (width // 2 - font_width // 2, height // 2 - font_height // 2),
            "NO DETECT",
            font = font_1,
            fill=MyColor.Color("BLACK"),
        )
    disp.image(img)



def ImageProcess():
    (w, h) = img.size
    for i in range(0, w-1):
        for j in range(0, h-1):
            (r,g,b) = img.getpixel((i, j))
            img.putpixel((i, j), (b, g, r))