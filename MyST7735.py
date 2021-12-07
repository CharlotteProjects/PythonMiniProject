#!/usr/bin/python

import MyColor
import time

# ST7735 library
import digitalio, board
import adafruit_rgb_display.st7735 as st7735

# Drawing library
from PIL import Image, ImageDraw, ImageFont

# Font
font_0 = ImageFont.truetype("Font/DejaVuSans.ttf", 12)
font_0a = ImageFont.truetype("Font/DejaVuSans.ttf", 16)
# DTH11
# login Title
font_1 = ImageFont.truetype('Font/AntiqueQuestSt.ttf',16)
# Member Name
font_2 = ImageFont.truetype('Font/DevinneSwash.ttf',14)
font_2a = ImageFont.truetype('Font/DevinneSwash.ttf',11)

font_3 = ImageFont.truetype('Font/Cretino.TTF', 12)
font_4 = ImageFont.truetype('Font/AceRecords.ttf',12)

floor_1 = False
floor_2 = False
floor_3 = False

# init the ST7735
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
    
        img = Image.open("Picture/background.jpg")
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
    
        img = Image.open("Picture/background.jpg")
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
    global floor_1
    global floor_2
    global floor_3
    global font_1
    font = font_1
    
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
    img = Image.open("Picture/background.jpg")
    # Load Image
    if floor_1:
        img_floor_1 = Image.open("Picture/light_on_1.jpg")
    else:
        img_floor_1 = Image.open("Picture/light_off_1.jpg")
        
    if floor_2:
        img_floor_2 = Image.open("Picture/light_on_2.jpg")
    else:
        img_floor_2 = Image.open("Picture/light_off_2.jpg")
        
    if floor_3:
        img_floor_3 = Image.open("Picture/light_on_3.jpg")
    else:
        img_floor_3 = Image.open("Picture/light_off_3.jpg")
    
    # Resize the picture
    img_floor_1 = img_floor_1.resize((18, 30), Image.ANTIALIAS)
    img_floor_2 = img_floor_2.resize((18, 30), Image.ANTIALIAS)
    img_floor_3 = img_floor_3.resize((18, 30), Image.ANTIALIAS)
    img = img.resize((width, height), Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)
    
    #draw.rectangle((0, 0, width, height), outline = MyColor.Color("BLACK"), fill = MyColor.Color("BLACK"))
    #draw.rectangle((BORDER, BORDER, width-BORDER, height-BORDER-1), outline = MyColor.Color("WHITE"), fill = MyColor.Color("WHITE"))
    
    text_temp = ("Temperature: %d C" % temperature)
    text_humi = ("Humidity: %d %%" % humidity)
    
    (font_width, font_height) = font.getsize(text_temp)
    draw.text(
        (5, 30),
        text_temp,
        font = font_0a,
        fill=MyColor.Color("BLACK"),
    )
    
    # Set center ==> (width // 2 - font_width // 2, height // 2 - font_height // 2)
    
    (font_width, font_height) = font.getsize(text_humi)
    draw.text(
        (5, 50),
        text_humi,
        font = font_0a,
        fill=MyColor.Color("BLACK"),
    )
    
    img.paste(img_floor_1, (106 ,0))
    img.paste(img_floor_2, (124 ,0))
    img.paste(img_floor_3, (142 ,0))
    disp.image(ImageProcess(img))   
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


# for change the color
def ImageProcess(image):
    (w, h) = image.size
    for i in range(0, w-1):
        for j in range(0, h-1):
            (r,g,b) = image.getpixel((i, j))
            image.putpixel((i, j), (b, g, r))
    return image

# setting the Float
def SetFloor(num, onOff):
    global floor_1
    global floor_2
    global floor_3
    if num == 1:
        if onOff:
            floor_1 = True
        else:
            floor_1 = False
            
    if num == 2:
        if onOff:
            floor_2 = True
        else:
            floor_2 = False
            
    if num == 3:
        if onOff:
            floor_3 = True
        else:
            floor_3 = False
    
    if not (num == 1 or num == 2 or num == 3):
        print("floor input error")
        floor_1 = False
        floor_2 = False
        floor_3 = False