import datetime
from base_state import BaseState

class SetTimeState(BaseState):
    def __init__(self, state_name, state_icon, home_state):
        self.set_edit_mode("H")
        self._H = False
        self._M = False
        self._S = False
        super().__init__(state_name, state_icon, home_state)

    def set_edit_mode(self, mode):
        now = datetime.datetime.now()
        self._mode = mode
        if self._mode == "H":
            if not self._H:
                self._H = now.strftime("%H")
        elif self._mode == "M":
            if not self._M:
                self._M = now.strftime("%M")
        else:
            if not self._S:
                self._S = now.strftime("%S")

    def up(self):
        if self._mode == "H":
            h = int(self._H)
            h = h+1
            if h > 23:
                h = 0
            self._H = str(h).zfill(2)
        elif self._mode == "M":
            m = int(self._M)
            m = m+1
            if m < 59:
                m = 0
            self._M = str(m).zfill(2)
        else:
            s = int(self._S)
            s = s+1
            if s > 59:
                s = 0
            self._S = str(s).zfill(2)
            
    def down(self):
        if self._mode == "H":
            h = int(self._H)
            h = h-1
            if h < 0:
                h = 23
            self._H = str(h).zfill(2)
        elif self._mode == "M":
            m = int(self._M)
            m = m-1
            if m < 0:
                m = 59
            self._M = str(m).zfill(2)
        else:
            s = int(self._S)
            s = s-1
            if s < 0:
                s = 59
            self._S = str(s).zfill(2)

    def left(self):
        if self._mode == "H":
           self.set_system_time()  
        elif self._mode == "M":
           self.set_edit_mode("H")  
        else:
           self.set_edit_mode("M")  

    def right(self):
        if self._mode == "H":
           self.set_edit_mode("M")  
        elif self._mode == "M":
           self.set_edit_mode("S")  

    def show_state(self, draw, width, height):
        now = datetime.datetime.now()
        if self._H:
            time_now = self._H
        else:
            time_now = now.strftime("%H")
        time_now += ":"
        if self._M:
            time_now += self._M
        else:
            time_now += now.strftime("%M")
        time_now += ":"
        if self._S:
            time_now += self._S
        else:
            time_now += now.strftime("%S")

        gap = 6
        wu,hu = draw.textsize(text="\uf105", font=BaseState.font_awesome_small)
        wd,hd = draw.textsize(text="\uf104", font=BaseState.font_awesome_small)
        wt,ht = draw.textsize(text=time_now)

        top = height - ht -gap - hu
        left = (width - wt) / 2
        draw.text((left, top), text=time_now, fill = "yellow")

        wc,hc = draw.textsize(text=":")
        wdd,hdd = draw.textsize(text="00")
        top = height -hd - gap - ht -gap - hu
        left = (width - wt) / 2
        if self._mode == "H": 
            left += (wdd - wu) / 2           
        elif self._mode == "M":
            left += ((wdd - wu) / 2) + wc + wdd           
        else:
            left += ((wdd - wu) / 2) + (wc + wdd) * 2

        draw.text((left, top), text="\uf105", font=BaseState.font_awesome_small, fill="yellow")
        top += hu + gap + ht + gap          
        draw.text((left, top), text="\uf104", font=BaseState.font_awesome_small, fill="yellow")           


