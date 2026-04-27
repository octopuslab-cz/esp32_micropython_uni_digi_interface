from micropython import const
from machine import Pin, I2C
from components.i2c_expander import Expander16
from utils.pinout import set_pinout
pinout = set_pinout()


def init_led(led_pin=2):
    from components.led import Led
    led = Led(led_pin)
    return led


def init_rgb(pin,num=1):
    from components.ws_rgb import Rgb
    ws = Rgb(10,num)
    # ws = Rgb(pinout.PWM2_PIN,16)
    return ws


def rgb_fill(ws, offset=0,c=(0,0,0)):
    for i in range(8):
        ws.color(c,i+offset)


def show_byte(ws, value, offset=8, reverse=True, color_on=(0,50,0), color_off=(0,0,0)):
    for i in range(8):
        bit = (value >> i) & 1  # i-bit (LSB = i=0)

        if reverse:
            idx = (7 - i) + offset
        else:
            idx = i + offset

        if bit:
            ws.color(color_on, idx)
        else:
            ws.color(color_off, idx)


def i2c_init(HW_or_SW=0,freq=100000):
    print("- i2c init")
    # I2C_SDA_PIN, I2C_SCL_PIN = const(21), const(22)
    print(pinout.I2C_SCL_PIN,pinout.I2C_SDA_PIN)
    i2c = I2C(scl=Pin(HW_or_SW, pinout.I2C_SCL_PIN), sda=Pin(pinout.I2C_SDA_PIN), freq=freq)

    # HW_or_SW: HW 0 | SW 1
    ## i2c = I2C(HW_or_SW, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=freq)
    return i2c


def lcd4_show(lcd,s="",r=0,c=0):
    lcd.move_to(c,r)
    lcd.putstr(s)


def lcd4_init():
    print("- lcd4_init")
    from lib.esp8266_i2c_lcd import I2cLcd
    lcd = I2cLcd(i2c, 63, 4, 16) # addr, rows, col
    lcd4_show(lcd, "octopusLab | s80") # write text
    lcd4_show(lcd, "****************",1)
      
    return lcd


def exp16_init(i2c):
     
    #clk = Led(26)
    b2 = bytearray(16 // 8) # temp 2 bytes    
    e16 = Expander16(39, i2c) # addr default 000 > 0x20
    
    return e16, b2