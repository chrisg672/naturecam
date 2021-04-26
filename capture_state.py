from datetime import datetime
from base_state import BaseState
from subprocess import call
from subprocess import Popen
from suntime import Sun
import pytz
import picamera
import time
import os

DEBUG = False

# Enter your longitude / latitude here
s = Sun(50.2939025,-4.9515043)

def ensure_dirs():
    if not os.path.exists('/home/pi/trailcam_log'):
        os.makedirs('/home/pi/trailcam_log')

    if not os.path.exists('/home/pi/videos'):
        os.makedirs('/home/pi/videos')

    usb = call('mountpoint -q /mnt/usb', shell=True)

    if usb == 0 and not os.path.exists('/mnt/usb/videos'):
        os.makedirs('/mnt/usb/videos')

# TODO - make settle time and capture duration configurable
# TODO - add video still capture mode
# TODO - add timelapse capture mode
class CaptureState(BaseState):
    def __init__(self, home_state):
        self._capturing_video = False
        self._settling = False
        ensure_dirs()
        super().__init__("capture", " ", home_state, BaseState.font_awesome, BaseState.font_awesome_small)
    
    def activate(self):
        self._start_settling(25)
        self._convert_process = None
        self._show_text = True
        super().activate()

    def down(self):
        self.motion_stopped()

    def up(self):
        self.motion_detected()

    def motion_detected(self):
        self.log_info("motion detected")
        if not self._capturing_video and not self._settling:
            self.start_capture_video()
        super().motion_detected()

    def start_capture_video(self):
        self._cam = picamera.PiCamera()
        self._cam.resolution = (1920,1024)
        self._cam.annotate_background = picamera.Color('black')
        self._cam.start_recording('/home/pi/video.h264')
        self.capture_end_at = time.mktime(datetime.now().utctimetuple()) + 20
        self._capturing_video = True

    def update_video(self):
        if self._capturing_video:
            if time.mktime(datetime.now().utctimetuple()) > self.capture_end_at:
                self.end_capture_video()
            else:
                self._cam.annotate_text = datetime.now().strftime('%d-%m-%y %H:%M:%S')
                self._cam.wait_recording(0.2)

    def end_capture_video(self):
        self._cam.close()
        self._cam = None
        self._capturing_video = True
        timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
        input_video = '/home/pi/video.h264'

        self.log_info('Attempting to save video')

        usb = call('mountpoint -q /mnt/usb', shell=True)

        if usb == 0:
            self.log_info('Saving to /mnt/usb/videos/')
            output_video = '/mnt/usb/videos/{}.mp4'.format(timestamp)
        else:
            self.log_info('Saving to /home/pi/videos/')
            output_video = '/home/pi/videos/{}.mp4'.format(timestamp)

        self._convert_process = Popen(['MP4Box', '-add', input_video, output_video])
        self._capturing_video = False
        self._start_settling(15)
        self._settling = True
        self._settle_after = time.mktime(datetime.now().utctimetuple()) + 10

    def _start_settling(self, duration):
        self._settling = True
        self._settle_after = time.mktime(datetime.now().utctimetuple()) + duration
        self._settle_duration = duration

    def settle_sensor(self):
        if self._settling:
            if self._convert_process != None and self._convert_process.poll() == None:
                return
            if time.mktime(datetime.now().utctimetuple()) > self._settle_after:
                self._settling = False  
                self._show_text = DEBUG 

    def set_camera_mode(self):
        if BaseState.camera_mode == 2:
            # Auto Mode
            sunset = s.get_sunset_time()
            sunrise = s.get_sunrise_time()
            now = datetime.now(pytz.timezone('Europe/London'))
            nightMode = (now.hour > sunset.hour or (now.hour == sunset.hour and now.minute > sunset.minute)) or \
                        (now.hour < sunrise.hour or (now.hour == sunrise.hour and now.minute < sunrise.minute))
            if nightMode:
                BaseState.CAMERA_CONTROL.off()
            else:
                BaseState.CAMERA_CONTROL.on()
        elif BaseState.camera_mode == 1:
            # Night Mode
            BaseState.CAMERA_CONTROL.off()
        else:
            # Day Mode     
            BaseState.CAMERA_CONTROL.on()

    def show_state(self, draw, width, height):
        self.settle_sensor()
        self.update_video()
        self.set_camera_mode()
        if self._show_text:
            message = "idle"
            now = time.mktime(datetime.now().utctimetuple())
            if self._capturing_video:
                elapsed = now + 20 - self.capture_end_at
                message = "recording " + str(int(elapsed)).zfill(2) + "/20"
            if self._settling:
                elapsed = now + self._settle_duration - self._settle_after
                message = "settling " + str(int(elapsed)).zfill(2) + "/" + str(int(self._settle_duration))
            wt,ht = draw.textsize(text="a");
            top = (height - ht) / 2
            self.centre_text(draw, width, top, message)
            self.show_motion_dot(draw, width, height)
