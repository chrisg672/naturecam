from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from gpiozero import Button
from base_state import BaseState
from time_state import TimeState
from set_time_state import SetTimeState
import os
from PIL import ImageFont

serial = i2c(port=1, address=0x3C)
display = ssd1306(serial)
UP_BUTTON = Button(13)
DOWN_BUTTON = Button(26)
LEFT_BUTTON = Button(6)
RIGHT_BUTTON = Button(0)
ACTION_BUTTON = Button(5)
HOME_BUTTON = Button(19)

home_state = BaseState("home", "\uf015", None)
settings_state = BaseState("settings", "\uf013", home_state)
set_capture_mode_state = BaseState("capture mode", "\uf030", home_state)
settings_time = BaseState("set time", "\uf017", home_state)
set_date_state = BaseState("set date", "\uf073", home_state)
arm_state = BaseState("arm", "\uf21b", home_state)
time_state = TimeState("time", "\uf017", home_state)
set_time_state = SetTimeState("set time", " ", home_state)
usb_state = BaseState("usb", "\uf287", home_state)
wifi_state = BaseState("wifi", "\uf1eb", home_state)

home_state.set_next_state(settings_state)
home_state.set_action_state(time_state)
settings_state.set_action_state(set_capture_mode_state)
set_capture_mode_state.set_next_state(settings_time)
settings_time.set_next_state(set_date_state)
settings_time.set_action_state(set_time_state)
set_date_state.set_next_state(usb_state)
usb_state.set_next_state(wifi_state)

# Work out height of text
text_height = 0
with canvas(display) as draw:
        w, text_height = draw.textsize(" ")

# prev icon (small)
# gap
# icon (large)
# gap
# text
# gap
# next icon (small)
gap = 3
available_height = display.height - 3 * gap - text_height
small_icon_size = int(available_height / 4)
large_icon_size = 2 * small_icon_size 

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

BaseState.font_awesome = make_font("fa-solid-900.ttf", large_icon_size)
BaseState.font_awesome_small = make_font("fa-solid-900.ttf", small_icon_size)

def up_pressed():
    BaseState.current_state.up()

def down_pressed():
    BaseState.current_state.down()

def left_pressed():
    BaseState.current_state.left()

def right_pressed():
    BaseState.current_state.right()

def action_pressed():
    BaseState.current_state.action()

def home_pressed():
    BaseState.current_state.home()

UP_BUTTON.when_pressed = up_pressed
DOWN_BUTTON.when_pressed = down_pressed
LEFT_BUTTON.when_pressed = left_pressed
RIGHT_BUTTON.when_pressed = right_pressed
ACTION_BUTTON.when_pressed = action_pressed
HOME_BUTTON.when_pressed = home_pressed

while BaseState.current_state.is_running():
    if BaseState.current_state.should_update():
        BaseState.current_state.show(display)
