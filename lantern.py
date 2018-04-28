import time

import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy


class TrainLantern:
    NUM_MODES = 5
    NUM_LED = 4
    BLACK = fancy.CRGB(0, 0, 0)
    RED = fancy.CRGB(255, 0, 0)
    YELLOW = fancy.CRGB(255, 255, 0)
    GREEN = fancy.CRGB(0, 200, 0)
    BLUE = fancy.CRGB(0, 0, 255)
    WHITE = fancy.CRGB(255, 255, 255)

    def __init__(self, pin, brightness, mode=0):
        """"""
        self.neopixels = neopixel.NeoPixel(pin,
                                           TrainLantern.NUM_LED,
                                           brightness=brightness,
                                           auto_write=False)
        self.mode = mode
        self.prev_mode = -1

        self.tick_delay = 0.25
        self.tick = 0
        self.prev_time = 0

        self._unit_speed = 0
        self._unit_counter_increment = 0
        self.unit_counter = 0
        self.unit_tick = 0

        self.button_latch = False

        # init
        self.clear()
        self.unit_speed = .5

    @property
    def unit_speed(self):
        return self._unit_speed

    @unit_speed.setter
    def unit_speed(self, value):
        self._unit_speed = value
        self._unit_counter_increment = value / 100
        # print("increment: {}".format(self._unit_counter_increment))

    def set_brightness(self, value):
        self.neopixels.brightness = max(value, 0.05)

    def toggle(self, button):
        if button and not self.button_latch:
            self.mode += 1
            if self.mode > TrainLantern.NUM_MODES:
                self.mode = 0
        self.button_latch = button

    def clear(self):
        self.neopixels.fill((0, 0, 0))
        self.neopixels.show()

    def update_tick(self):
        current_time = time.monotonic()
        delta = current_time - self.prev_time
        if delta > self.tick_delay:
            self.tick += 1
            if self.tick >= TrainLantern.NUM_LED:
                self.tick = 0
            # print("tick: {}".format(self.tick))
            self.prev_time = current_time
        self.unit_counter += self._unit_counter_increment
        if self.unit_counter > 1:
            self.unit_counter = 0
            self.unit_tick += 1
            if self.unit_tick >= TrainLantern.NUM_LED:
                self.unit_tick = 0

    def run(self):
        if self.mode != self.prev_mode:
            self.clear()
            time.sleep(0.35)
        try:
            method_to_call = getattr(self, "mode_{}".format(self.mode))
            method_to_call()
        except AttributeError as e:
            print(e)
            self.mode_0()
        self.prev_mode = self.mode

    def mode_0(self):
        """ all on, one red, one yellow, one blue, one green"""
        self.neopixels[3] = fancy.gamma_adjust(TrainLantern.RED).pack()
        self.neopixels[0] = fancy.gamma_adjust(TrainLantern.YELLOW).pack()
        self.neopixels[1] = fancy.gamma_adjust(TrainLantern.BLUE).pack()
        self.neopixels[2] = fancy.gamma_adjust(TrainLantern.GREEN).pack()
        self.neopixels.show()

    def mode_1(self):
        """ red cycle around """
        self.tick_delay = 0.25
        for i in range(self.NUM_LED):
            color = TrainLantern.RED if i == self.tick else TrainLantern.BLACK
            self.neopixels[i] = color.pack()
        self.neopixels.show()
        self.update_tick()

    def mode_2(self):
        """ alternate red and yellow """
        self.tick_delay = 1
        for i in range(self.NUM_LED):
            i_mod = i % 2
            if self.tick % 2:
                color = TrainLantern.BLACK if i_mod else TrainLantern.YELLOW
            else:
                color = TrainLantern.RED if i_mod else TrainLantern.BLACK
            self.neopixels[i] = fancy.gamma_adjust(color).pack()
        self.neopixels.show()
        self.update_tick()

    def mode_3(self):
        """ front full white, others alternate """
        self.tick_delay = 0.25
        self.unit_speed = 0.5
        for i in range(self.NUM_LED):
            if i == 3:
                color = TrainLantern.WHITE
            else:
                color = fancy.gamma_adjust(fancy.CHSV(self.unit_counter))
            self.neopixels[i] = color.pack()
        self.neopixels.show()
        self.update_tick()

    def mode_4(self):
        """ front red, back green, sides flashing yellow """
        self.tick_delay = 1
        dim_yellow = fancy.gamma_adjust(TrainLantern.YELLOW, brightness=(0.25, 0.25, 0.25))
        tick_mod = self.tick % 2
        self.neopixels[3] = TrainLantern.RED.pack()
        self.neopixels[0] = dim_yellow.pack() if tick_mod else TrainLantern.BLACK.pack()
        self.neopixels[1] = TrainLantern.GREEN.pack()
        self.neopixels[2] = TrainLantern.BLACK.pack() if tick_mod else dim_yellow.pack()
        self.neopixels.show()
        self.update_tick()

    def mode_5(self):
        """ hue cycle """
        for i in range(TrainLantern.NUM_LED):
            hue = self.unit_counter + (0.25*i)
            if hue > 1:
                hue -= 1
            color = fancy.CHSV(hue)
            self.neopixels[i] = color.pack()
        self.neopixels.show()
        self.update_tick()
