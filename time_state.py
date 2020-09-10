import datetime
import psutil
from base_state import BaseState
from luma.core.render import canvas

class TimeState(BaseState):
    def __init__(self, home_state):
        self.date_now = ""
        self.time_now = ""
        super().__init__("time", " ", home_state, BaseState.font_awesome, BaseState.font_awesome_small)

    def handleAnyInput(self):
        self.home()

    def should_update(self):
        now = datetime.datetime.now()
        date_now = now.strftime("%d %b %y")
        time_now = now.strftime("%H:%M:%S")
        if (time_now != self.time_now or date_now != self.date_now):
            self.time_now = time_now
            self.date_now = date_now
            return True
        return False

    def show(self, display):
        with canvas(display) as draw:
            self.show_time(draw, display.width, display.height)

    def show_time(self, draw, width, height):
        gap = 6
        address = psutil.net_if_addrs()["wlan0"][0].address
        wd, hd = draw.textsize(self.date_now)
        wt, ht = draw.textsize(self.time_now)
        wa, ha = draw.textsize(address)
        
        left = (width - wt) / 2
        top = (height - ht - hd - ha - gap - gap) / 2
        draw.text((left, top), self.time_now, fill="yellow")
        
        left = (width - wd) / 2
        top = top + ht + gap
        draw.text((left, top), self.date_now, fill="yellow")
        
        left = (width - wa) / 2
        top = top + hd + gap
        draw.text((left, top), address, fill="yellow")