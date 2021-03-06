from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from gpiozero import Button
from gpiozero import MotionSensor
from gpiozero import DigitalOutputDevice
from base_state import BaseState
from show_time_ip_state import ShowTimeIpState
from set_time_state import SetTimeState
from set_date_state import SetDateState
from capture_state import CaptureState
from add_wifi_network import AddWiFiNetwork
from set_camera_mode_state import SetCameraModeState
from set_camera_record_time_state import SetCameraRecordTimeState
import os
from PIL import ImageFont
import logging
from datetime import datetime

logdir = '/home/pi/trailcam_log'
logfile = logdir + '/trailcam_log-'+str(datetime.now().strftime('%Y%m%d-%H%M'))+'.csv'
logging.basicConfig(filename=logfile, level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d, %H:%M:%S,')

serial = i2c(port=1, address=0x3C)
display = ssd1306(serial)
UP_BUTTON = Button(13)
DOWN_BUTTON = Button(26)
LEFT_BUTTON = Button(6)
RIGHT_BUTTON = Button(0)
ACTION_BUTTON = Button(5)
HOME_BUTTON = Button(19)
PIR = MotionSensor(23)
# Camera Mode High => Day Mode, Low => Night Mode
CAMERA_CONTROL = DigitalOutputDevice(21, True, True)

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

# 0 = Day, 1 = Night, 2 = Auto
BaseState.camera_mode = 2 # AUTO
BaseState.CAMERA_CONTROL = CAMERA_CONTROL

BaseState.capture_duration = 20 # 20s capture times

# HOME 
home_state = BaseState("home", "\uf015", None, BaseState.font_awesome, BaseState.font_awesome_small)
home_state.load_settings() # loads current settings into BaseState
#     HOME -> SHOW-TIME-IP
show_time_ip_state = ShowTimeIpState(home_state)
home_state.set_action_state(show_time_ip_state)

# HOME (down) START-CAPTURE
start_capture_state = BaseState("start capture", "\uf030", home_state, BaseState.font_awesome, BaseState.font_awesome_small)
home_state.set_next_state(start_capture_state)
# START-CAPTURE -> SET-CAMERA-MODE
set_camera_mode_state = SetCameraModeState(home_state)
start_capture_state.set_action_state(set_camera_mode_state)
#    SET-CAMERA-MODE -> SET-CAPTURE-TIME
set_camera_record_time_state = SetCameraRecordTimeState(home_state)
set_camera_mode_state.set_action_state(set_camera_record_time_state)
#       SET-CAPTURE-TIME -> CAPTURING
capture_state = CaptureState(home_state)
set_camera_record_time_state.set_action_state(capture_state)

# START-CAPTURE (down) SETTINGS
settings_state = BaseState("settings", "\uf013", home_state, BaseState.font_awesome, BaseState.font_awesome_small)
start_capture_state.set_next_state(settings_state)

# SETTINGS -> SET-TIME
settings_time = BaseState("set time", "\uf017", home_state, BaseState.font_awesome, BaseState.font_awesome_small)
settings_state.set_action_state(settings_time)
#    SET-TIME -> ACTUALLY SET TIME
set_time_state = SetTimeState(home_state)
settings_time.set_action_state(set_time_state)

#    SET-TIME (down) SET-DATE
settings_date = BaseState("set date", "\uf073", home_state, BaseState.font_awesome, BaseState.font_awesome_small)
settings_time.set_next_state(settings_date)
#       SET-DATE -> ACTUALLY SET DATE
set_date_state = SetDateState(home_state)
settings_date.set_action_state(set_date_state)

#    SET-DATE (down) SET-WIFI
settings_wifi = BaseState("pair wifi", "\uf1eb", home_state, BaseState.font_awesome, BaseState.font_awesome_small)
settings_date.set_next_state(settings_wifi)
#       SET-WIFI -> ADD-WIFI
add_wifi_network = AddWiFiNetwork(home_state)
settings_wifi.set_action_state(add_wifi_network)

def up_pressed():
    BaseState.current_state.up()
    logging.info("up -> state = "+ BaseState.current_state.name())

def down_pressed():
    BaseState.current_state.down()
    logging.info("down -> state = "+ BaseState.current_state.name())

def left_pressed():
    BaseState.current_state.left()

def right_pressed():
    BaseState.current_state.right()

def action_pressed():
    BaseState.current_state.action()

def home_pressed():
    BaseState.current_state.home()

def motion_detected():
    BaseState.current_state.motion_detected()

def motion_stopped():
    BaseState.current_state.motion_stopped()

UP_BUTTON.when_pressed = up_pressed
DOWN_BUTTON.when_pressed = down_pressed
LEFT_BUTTON.when_pressed = left_pressed
RIGHT_BUTTON.when_pressed = right_pressed
ACTION_BUTTON.when_pressed = action_pressed
HOME_BUTTON.when_pressed = home_pressed
PIR.when_motion = motion_detected
PIR.when_no_motion = motion_stopped
BaseState.pir = PIR

while BaseState.current_state.is_running():
    if BaseState.current_state.should_update():
        BaseState.current_state.show(display)
