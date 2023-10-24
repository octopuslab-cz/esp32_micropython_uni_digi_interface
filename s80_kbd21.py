# TM1638 example
"""
MVI_A 0b10101010 ; intro:
MOV_A,A          ; show acc -> 10101010
3e aa 7f
-------------------

3e aa 7f 5b 2f 7f 5b c3 00 00 00 
"""

from time import sleep
from lib.tm1638 import TM1638
from machine import Pin
from components.kbd21c import Hex2, BTN_TAB
from components.microprocessor.s80 import table
from components.microprocessor.s80.core import __version__, Executor, create_hex_program, print_hex_program, parse_file, run_hex_code

from utils.bits import neg, reverse, set_bit, get_bit
from utils.pinout import set_pinout

pinout = set_pinout()

# right OCTOBUS SCI:
# STB = MOSI 23
# CLK = MISO 19
# DIO = SCLK 18

print("--- TM1638 - KBD21 ---")

tm = TM1638(stb=Pin(pinout.SPI_MOSI_PIN), clk=Pin(pinout.SPI_MISO_PIN), dio=Pin(pinout.SPI_CLK_PIN))

num = 0
uP = Executor()

h2 = Hex2()

"""
def format_digit(dig):
   return (8-len(str(dig)))*" "+str(dig) 


def add_digit(dig):
   global num
   if dig >= 0:
     try:
        num = num*10 + (int(dig))
        rnum = num
     except:
        rnum = 0
   else:
      rnum = 0
   return rnum 
"""


tm.show(" rUr8bit") # 8bIt rUr
sleep(2)
btn_val = " "
tm.show2(" "*8)

while True:
    btn_read = tm.keys()
      
    if btn_read[0] > 0:
       print(btn_read)
       
       btn_val = BTN_TAB[btn_read]
                 
       if btn_val == "-" or  btn_val == "P" or  btn_val == "R":
           if btn_val == "-":
               h2.dec()               
           if btn_val == "P":
               h2.inc()
           if btn_val == "R":
               print("--- RUN ---")
               #print(h2.get_saved_arr(), h2.saved_hex2_index)
               hex_program = h2.get_saved_program()
               print("HEX",hex_program)
               num_program = h2.get_program_num()
               print("INT",num_program)
               
               print("="*32)
               run_hex_code(uP,num_program,run_delay_ms=0) # todo HEX
               sleep(3)
     
           #show index+1
           try:    
               str_show = "{:0>4}".format(str(h2.saved_hex2_index+1)) + "  " + h2.get_saved_hex2(h2.saved_hex2_index)
               print("-"*5,h2.get_saved_hex2(h2.saved_hex2_index),str_show)
               tm.show2(str_show)
           except:
               print("err")
       else:
           h2.add(btn_val)
           if btn_val == "S":
               tm.show2("S")
               sleep(0.3)
           #str_show = "{:0>4}".format(str(h2.saved_hex2_index)) + "  " + h2.get_saved_hex2(h2.saved_hex2_index)
           tm.show2("{:0>4}".format(str(h2.saved_hex2_index+1)) + "  " + h2.show())
           #tm.show2(str_show)
           
       print("test23",btn_val)
       print(h2.get_saved_arr(), h2.saved_hex2_index)
       sleep(0.1)
        
       """
       if btn_val == "C": num  = add_digit(-1)
       if btn_val == "E": 
          print("publish: ", num)
       
       if btn_val != "C" and btn_val != "E":
           num = add_digit(int(btn_val))
           tm.show2(format_digit(num))
           sleep(0.5)
       num = btn_val
       """       
    sleep(0.1)
    #print("keys: " + str(tm.keys())
    #tm.show2(format_digit(btn_val))
