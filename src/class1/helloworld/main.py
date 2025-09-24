from machine import Pin, I2C
from libs.lib import TerminalDisplay

# Boring Setup Stuff
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
display = TerminalDisplay(width=128, height=64, i2c=i2c, addr=0x3C)

# example 1: hello world to display
display.write("hello world!")

# example 2: writing multiple lines
display.write("hello world!")
display.write("hello more world!")

# example 3: printing to terminal vs display
display.write("hello world!")
print("where is this?")

# example 4: simple string variable
m = "testing"
display.write(m)

# example 5: overwriting variable
m = "this?"
m = "that"
display.write(m)

# example 6: print multiple with one variable
m = "this?"
display.write(m)
m = "that"
display.write(m)

# example 7: An error occured!
display.write(x)
x = "1234"
