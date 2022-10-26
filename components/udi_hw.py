from micropython import const


def init_led(led_pin=2):
    from components.led import Led
    led = Led(led_pin)
    return led


def i2c_init(HW_or_SW=0,freq=100000):
    print("- i2c init")
    from machine import Pin, I2C
    I2C_SDA_PIN, I2C_SCL_PIN = const(21), const(22)
    # HW_or_SW: HW 0 | SW 1
    i2c = I2C(HW_or_SW, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=freq)
    return i2c


def lcd4_show(lcd,s="",r=0,c=0):
    lcd.move_to(c,r)
    lcd.putstr(s)


def lcd4_init(i2c):
    print("- lcd4_init")
    from lib.esp8266_i2c_lcd import I2cLcd
    lcd = I2cLcd(i2c, 63, 4, 16) # addr, rows, col
    lcd4_show(lcd, "octopusLab | s80") # write text
    lcd4_show(lcd, "****************",1)
      
    return lcd