# test_ws | pwm2 = 10
            
from components.udi_hw import init_rgb, rgb_fill, show_byte
from time import sleep

ws = init_rgb(10,16)
offset = 8
       
        
# ws.rainbow_cycle()
rgb_fill(ws,offset,(50,0,0))
sleep(1)
rgb_fill(ws,offset,(0,0,0))

for i in range(100):
    show_byte(ws, i)
    sleep(0.3)