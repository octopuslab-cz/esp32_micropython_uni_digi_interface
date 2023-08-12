# This file is part of the octopusLAB project
# The MIT License
# (c) 2016-2021 Jan Copak, Petr Kracik, Vasek Chalupnicek

# from mini_terminal import terminal_info...
import sys

__version__ = "1.0.1"

SEPARATOR_WIDTH = 39

# --- VT 100 ---
def get_cursor_position():
    height=0
    width=0
    num=''

    sys.stdout.write('\x1b[6n')
    while True:
        char = sys.stdin.read(1)
        if char is 'R':
            width = int(num)
            break
        if char is '\x1b':
            width=0
            height=0
            num=''
            continue
        if char is '[':
            continue
        if char is ';':
            height=int(num)
            num=''
            continue
        num+=char
    return (width, height)


def terminal_info():
    # Save cursor position
    sys.stdout.write('\x1b[s')
    
    #Move cursor outside of screen
    sys.stdout.write('\x1b[999B\x1b[999C')
    (w, h) = get_cursor_position()
    
    # Restore cursor position
    sys.stdout.write('\x1b[u')

    print ("terminal_size: ", w, h)
 
 
def terminal_clear():
    # def clear():
    print(chr(27) + "[2J")  # clear terminal
    print("\x1b[2J\x1b[H")  # cursor up


def terminal_color(txt,col=33): # default yellow
    # 30 black / 31 red / 32 green / 33 yellow / 34 blue / 35 violet / 36 cyan 
    # 21 underline
    # print("\033[32mgreen\033[m")
    return "\033[" + str(col) + "m" + str(txt) + "\033[m"


def runningEffect(num = 16):
    from time import sleep_ms
    for ii in range(num):
        print(".",end="")
        sleep_ms(20)
    print()


def printBar(num1,num2,char="|",col1=32,col2=33):
    print("[",end="")
    print((("\033[" + str(col1) + "m" + str(char) + "\033[m")*num1),end="")
    print((("\033[" + str(col2) + "m" + str(char) + "\033[m")*num2),end="")
    print("]  ",end="")


# ---------------

def printHead(s):
    print()
    print('-' * SEPARATOR_WIDTH)
    print("[--- " + s + " ---] ")


def printTitle(t,w=SEPARATOR_WIDTH):
    print()
    print('=' * w)
    print("|",end="")
    print(t.center(w-2),end="")
    print("|")
    print('=' * w)


def printLog(i,s=""):
    print()
    print('-' * SEPARATOR_WIDTH)
    print("[--- " + str(i) + " ---] " + s)