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

verses = []
verses.append("In the beginning was the Word, and the Word was with God, and the Word was God.".split())
verses.append("He was with God in the beginning.".split())
verses.append("Through him all things were made; without him nothing was made that has been made.".split())


display.clear()
display.write("John 1:1")
i = 0
j = 0
pressed1 = False
while True:
    if button1.pressed():
        display.write(verses[j][i])
        i = (i + 1) % len(verses[j])
        while button1.pressed():
            continue
    if button2.pressed():
        print((i,j))
        j = (j + 1) % len(verses)
        i = 0
        display.write("John 1:"+str(j+1))
        while button2.pressed():
            continue
    if button3.pressed():
        print((i,j))
        j = (j - 1) % len(verses)
        if j < 0:
            j = len(verses) - 1
        i = 0
        display.write("John 1:"+str(j+1))
        while button3.pressed():
            continue
