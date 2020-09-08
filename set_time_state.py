import datetime
from base_state import BaseState

class SetTimeState(BaseState):
    def __init__(self, state_name, state_icon, home_state):
        super().__init__(state_name, state_icon, home_state)

    def activate(self):
        self.HH = False
        self.MM = False
        self.SS = False
        self.set_edit_mode("H")
        super()

    def set_edit_mode(self, mode):
        now = datetime.datetime.now()
        self._mode = mode
        if self._mode == "H":
            if not self.HH:
                self.HH = now.strftime("%H")
        elif self._mode == "M":
            if not self.MM:
                self.MM = now.strftime("%M")
        else:
            if not self.SS:
                self.SS = now.strftime("%S")

    def up(self):
        if self._mode == "H":
            h = int(self.HH)
            h = h+1
            if h > 23:
                h = 0
            self.HH = str(h).zfill(2)
        elif self._mode == "M":
            m = int(self.MM)
            m = m+1
            if m > 59:
                m = 0
            self.MM = str(m).zfill(2)
        else:
            s = int(self.SS)
            s = s+1
            if s > 59:
                s = 0
            self.SS = str(s).zfill(2)
            
    def down(self):
        if self._mode == "H":
            h = int(self.HH)
            h = h-1
            if h < 0:
                h = 23
            self.HH = str(h).zfill(2)
        elif self._mode == "M":
            m = int(self.MM)
            m = m-1
            if m < 0:
                m = 59
            self.MM = str(m).zfill(2)
        else:
            s = int(self.SS)
            s = s-1
            if s < 0:
                s = 59
            self.SS = str(s).zfill(2)

    def set_system_time(self):
        print ("time" +self.HH+":"+self.MM+":"+self.SS)

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
        if self.HH:
            time_now = self.HH
        else:
            time_now = now.strftime("%H")
        time_now += ":"
        if self.MM:
            time_now += self.MM
        else:
            time_now += now.strftime("%M")
        time_now += ":"
        if self.SS:
            time_now += self.SS
        else:
            time_now += now.strftime("%S")

        gap = 6
        wu,hu = draw.textsize(text="\uf077", font=BaseState.font_awesome_small)
        wd,hd = draw.textsize(text="\uf078", font=BaseState.font_awesome_small)
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

        draw.text((left, top), text="\uf077", font=BaseState.font_awesome_small, fill="yellow")
        top += hu + gap + ht + gap          
        draw.text((left, top), text="\uf078", font=BaseState.font_awesome_small, fill="yellow")           


