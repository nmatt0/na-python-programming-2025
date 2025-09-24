from ssd1306 import SSD1306_I2C
from machine import Pin
import time

class TerminalDisplay:
    def __init__(self, width=128, height=64, i2c=None, addr=0x3C):
        """Initialize the SSD1306 display with I2C."""
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.oled = SSD1306_I2C(width, height, i2c, addr=addr)
        self.char_width = 8  # Default font: 8 pixels wide
        self.char_height = 8  # Default font: 8 pixels tall
        self.cols = width // self.char_width  # e.g., 128/8 = 16 chars
        self.rows = height // self.char_height  # e.g., 64/8 = 8 rows
        self.lines = [""] * self.rows  # Buffer for current lines
        self.current_row = 0  # Tracks next free row
        self.clear()

    def clear(self):
        """Clear the screen and reset the line buffer."""
        self.oled.fill(0)
        self.oled.show()
        self.lines = [""] * self.rows
        self.current_row = 0

    def _split_into_lines(self, message, linewrap):
        """Split message into lines, respecting linewrap and column limits."""
        if not linewrap:
            # Truncate to fit one line
            return [message[:self.cols]]
        
        words = message.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + (1 if current_line else 0) <= self.cols:
                # Add word to current line
                current_line += (" " if current_line else "") + word
            else:
                # Start new line
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # Split long single words
        final_lines = []
        for line in lines:
            while len(line) > self.cols:
                final_lines.append(line[:self.cols])
                line = line[self.cols:]
            if line:
                final_lines.append(line)
        
        return final_lines

    def write(self, message, linewrap=True):
        """Write message to the screen, stacking lines and scrolling if needed."""
        lines = self._split_into_lines(message, linewrap)
        
        for line in lines:
            if self.current_row >= self.rows:
                # Scroll: shift lines up
                self.lines.pop(0)
                self.lines.append("")
                self.current_row -= 1
                # Redraw all lines
                self.oled.fill(0)
                for i, text in enumerate(self.lines):
                    if text:
                        self.oled.text(text, 0, i * self.char_height)
            
            # Add new line
            self.lines[self.current_row] = line
            self.oled.text(line, 0, self.current_row * self.char_height)
            self.current_row += 1
        
        self.oled.show()

class Button:
    def __init__(self, pin_number, debounce_ms=50, active_low=True):
        """Initialize button on specified GPIO pin with debouncing."""
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP if active_low else None)
        self.debounce_ms = debounce_ms
        self.active_low = active_low
        self.last_state = self._read_pin()
        self.last_debounce_time = time.ticks_ms()

    def _read_pin(self):
        """Read raw pin state (inverted for active-low)."""
        return not self.pin.value() if self.active_low else self.pin.value()

    def pressed(self):
        """Return True if button is pressed, False otherwise, with debouncing."""
        current_state = self._read_pin()
        current_time = time.ticks_ms()
        
        # Check if enough time has passed for debouncing
        if time.ticks_diff(current_time, self.last_debounce_time) >= self.debounce_ms:
            if current_state != self.last_state:
                self.last_debounce_time = current_time
                self.last_state = current_state
            return current_state
        return self.last_state