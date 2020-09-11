from datetime import datetime
from base_state import BaseState
from subprocess import call
import picamera
import time
import os

def ensure_dirs():
    if not os.path.exists('/home/pi/trailcam_log'):
        os.makedirs('/home/pi/trailcam_log')

    if not os.path.exists('/home/pi/videos'):
        os.makedirs('/home/pi/videos')

    if not os.path.exists('/mnt/usb/videos'):
        os.makedirs('/mnt/usb/videos')

def capture_video():
    ts = '{:%Y%m%d-%H%M%S}'.format(datetime.now())
    self.log_info('Beginning capture: '+ str(ts)+'.h264')
    with picamera.PiCamera() as cam:
        cam.resolution=(1920, 1024)
        cam.annotate_background = picamera.Color('black')

        cam.start_recording('/home/pi/video.h264')
        start = datetime.now()
        while (datetime.now() - start).seconds < duration:
            print (datetime.now() - start).seconds 
            cam.annotate_text = datetime.now().strftime('%d-%m-%y %H:%M:%S')
            cam.wait_recording(0.2)
        cam.stop_recording()
    time.sleep(1)
    log_info('Stopped recording')
    timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    input_video = '/home/pi/video.h264'

    log_info('Attempting to save video')

    usb = call('mountpoint -q /mnt/usb', shell=True)

    if usb == 0:
        self.log_info('Saving to /mnt/usb/videos/')
        output_video = '/mnt/usb/videos/{}.mp4'.format(timestamp)
    else:
        self.log_info('Saving to /home/pi/videos/')
        output_video = '/home/pi/videos/{}.mp4'.format(timestamp)

    call(['MP4Box', '-add', input_video, output_video])

class CaptureState(BaseState):
    def __init__(self, state_name, state_icon, home_state, font, font_small):
        self.capturing_video = False
        self.settling = False
        ensure_dirs()
        super().__init__("capture", " ", home_state, BaseState.font_awesome, BaseState.font_awesome_small)
    
    def activate(self):
        self.start_settling(60)
        super().activate()

    def motion_detected(self):
        if not self.capturing_video and not self.settling:
            self.start_capture_video()
        super().motion_detected()

    def start_capture_video():
        self.capturing_video = True
        self.cam = picamera.PiCamera()
        self.cam.resolution = (1920,1024)
        self.cam.annotate_background = picamera.Color('black')
        self.cam.start_recording('/home/pi/video.h264')
        self.capture_end_at = time.mktime(datetime.now().utctimetuple()) + 20

    def update_video(self):
        if self.capturing_video:
            if time.mktime(datetime.now().utctimetuple()) > self.capture_end_at:
                self.end_capture_video()
            else:
                self.cam.annotate_text = datetime.now().strftime('%d-%m-%y %H:%M:%S')
                self.cam.wait_recording(0.2)

    def end_capture_video(self):
        # Do we need to close() the camera?
        self.cam = None
        self.capturing_video = True
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

        call(['MP4Box', '-add', input_video, output_video])
        self.capturing_video = False
        self.start_settling(10)
        self.settling = True
        self.settle_after = time.mktime(datetime.now().utctimetuple()) + 10

    # Old method
    def capture_video():
        ts = '{:%Y%m%d-%H%M%S}'.format(datetime.now())
        self.log_info('Beginning capture: '+ str(ts)+'.h264')
        with picamera.PiCamera() as cam:
            cam.resolution=(1920, 1024)
            cam.annotate_background = picamera.Color('black')

            cam.start_recording('/home/pi/video.h264')
            start = datetime.now()
            while (datetime.now() - start).seconds < duration:
                print (datetime.now() - start).seconds 
                cam.annotate_text = datetime.now().strftime('%d-%m-%y %H:%M:%S')
                cam.wait_recording(0.2)
            cam.stop_recording()
        time.sleep(1)
        self.log_info('Stopped recording')
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

        call(['MP4Box', '-add', input_video, output_video])
        self.capturing_video = False
        self.settling = True
        self.settle_after = time.mktime(datetime.now().utctimetuple()) + 10

    def start_settling(self, duration):
        self.settling = True
        self.settle_after = time.mktime(datetime.now().utctimetuple()) + duration
        self.settle_duration = duration

    def settle_sensor(self):
        if self.settling:
            if time.mktime(datetime.now().utctimetuple()) > self.settle_after:
                self.settling = False        

    def show_state(self, draw, width, height):
        self.settle_sensor()
        self.update_video()
        message = "idle"
        now = time.mktime(datetime.now().utctimetuple())
        if self.capturing_video:
            elapsed = now + 20 - self.capture_end_at
            message = "recording " + elapsed + " / 20"
        if self.settling:
            elapsed = now + self.settle_duration - self.settle_after
            message = "settling " + elapsed + " / " + self.settle_duration
        self.centre_text(darw, width, height, message)
        self.show_motion_dot)(draw, width, height)
