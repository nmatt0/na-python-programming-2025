# main.py
# Display text, rectangle, and scrolling message on SSD1306 OLED (128x64) using I2C
from machine import Pin, I2C
from lib import TerminalDisplay, Button
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
display = TerminalDisplay(width=128, height=64, i2c=i2c, addr=0x3C)

# Initialize button on GP15
button1 = Button(pin_number=15, debounce_ms=50, active_low=True)
button2 = Button(pin_number=14, debounce_ms=50, active_low=True)
button3 = Button(pin_number=16, debounce_ms=50, active_low=True)
button4 = Button(pin_number=17, debounce_ms=50, active_low=True)


display.clear()
display.write("RACE!")
line1 = "1: "
line2 = "2: "
line3 = "3: "
display.write(line1)
display.write(line2)
display.write(line3)
win = False
pressed1 = False
while not win:
    if button1.pressed():
        line1 += "-"
        display.clear()
        display.write("RACE!")  
        display.write(line1)
        display.write(line2)
        display.write(line3)
        while button1.pressed():
            continue
    if button2.pressed():
        line2 += "-"
        display.clear()
        display.write("RACE!")  
        display.write(line1)
        display.write(line2)
        display.write(line3)
        while button2.pressed():
            continue
    if button3.pressed():
        line3 += "-"
        display.clear()
        display.write("RACE!")  
        display.write(line1)
        display.write(line2)
        display.write(line3)
        while button3.pressed():
            continue
    if len(line1) > 15:
        win = True
        display.write("1 WINS!")
    if len(line2) > 15:
        win = True
        display.write("2 WINS!")
    if len(line3) > 15:
        win = True
        display.write("3 WINS!")

