# test_ws | pwm2 = 10
            
from components.ws_rgb import Rgb
from time import sleep
from utils.pinout import set_pinout

pinout = set_pinout()
# ws = Rgb(10,16)
ws = Rgb(pinout.PWM2_PIN,16)

offset = 8

def rgb_fill(ws, c=(0,0,0)):
    for i in range(8):
        ws.color(c,i+offset)
        
        
# ws.rainbow_cycle()
rgb_fill(ws,(50,0,0))
sleep(5)
rgb_fill(ws,(0,0,0))