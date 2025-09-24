from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import random

# Initialize I2C and SSD1306 display (assuming 128x64 display on I2C0, SDA=GP0, SCL=GP1)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = SSD1306_I2C(128, 64, i2c)

# Button setup (assuming pull-up resistors, active low; change pins as needed)
# Up: GP2, Down: GP3, Left: GP4, Right: GP5
button_right = Pin(15, Pin.IN, Pin.PULL_UP)
button_left = Pin(14, Pin.IN, Pin.PULL_UP)
button_down = Pin(16, Pin.IN, Pin.PULL_UP)
button_up = Pin(17, Pin.IN, Pin.PULL_UP)

# Game settings
width = 16  # Grid width (128 / 8)
height = 8  # Grid height (64 / 8)
block_size = 8  # Pixel size per block

# Initial snake position (list of (x, y) tuples)
snake = [(2, 1), (1, 1), (0, 1)]

# Initial direction (right)
direction = (1, 0)

# Initial food position
food = (random.randint(0, width-1), random.randint(0, height-1))

# Function to draw the game
def draw():
    oled.fill(0)  # Clear display
    # Draw snake
    for seg in snake:
        oled.fill_rect(seg[0] * block_size, seg[1] * block_size, block_size, block_size, 1)
    # Draw food
    oled.fill_rect(food[0] * block_size, food[1] * block_size, block_size, block_size, 1)
    oled.show()

# Game loop
running = True
while running:
    # Check buttons (polling; only change direction if button pressed)
    if button_up.value() == 0 and direction != (0, 1):  # Prevent reverse
        direction = (0, -1)
    elif button_down.value() == 0 and direction != (0, -1):
        direction = (0, 1)
    elif button_left.value() == 0 and direction != (1, 0):
        direction = (-1, 0)
    elif button_right.value() == 0 and direction != (-1, 0):
        direction = (1, 0)
    
    # Calculate new head position
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    
    # Check for wall collision
    if (new_head[0] < 0 or new_head[0] >= width or
        new_head[1] < 0 or new_head[1] >= height):
        running = False
    
    # Check for self collision
    if new_head in snake:
        running = False
    
    if running:
        # Add new head
        snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == food:
            # Generate new food (simple, may overlap snake rarely)
            food = (random.randint(0, width-1), random.randint(0, height-1))
        else:
            # Remove tail
            snake.pop()
        
        # Draw updated game
        draw()
    
    # Game speed (adjust as needed)
    time.sleep(.4)

# Game over screen
oled.fill(0)
oled.text("Game Over", 30, 28, 1)
oled.show()