import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import lantern

# PINS #################################################################################################################
led_board = DigitalInOut(board.D13)
led_board.direction = Direction.OUTPUT

button = DigitalInOut(board.D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

led_button = DigitalInOut(board.D1)
led_button.direction = Direction.OUTPUT

potentiometer = AnalogIn(board.SCK)  # this is actually pin A3 but there is no alias for it...

# OBJECTS ##############################################################################################################
train_lantern = lantern.TrainLantern(board.D4, 1.0)

# MAIN LOOP ############################################################################################################
while True:
    led_board.value = led_button.value = not button.value
    train_lantern.toggle(not button.value)
    train_lantern.set_brightness(1-(potentiometer.value / 65536))
    train_lantern.run()
