from base_state import BaseState

class SetDateTimeBaseState(BaseState):
    def __init__(self, state_name, home_state):
        self.min = [0,0,0]
        self.max = [23,59,59]
        super().__init__(state_name, " ", home_state, BaseState.font_awesome, BaseState.font_awesome_small)

    def set_edit_mode(self, mode):
        self._mode = mode

    def up(self):
        self.time[self._mode] += 1
        self.normalise()
    
    def down(self):
        self.time[self._mode] -= 1
        self.normalise()

    def isValid(self):
        return True

    def normalise(self):
        for i in range(0,2):
            if self.time[i] < self.min[i]:
                self.time[i] = self.max[i]
            if self.time[i] > self.max[i]:
                self.time[i] = self.min[i]

    def set_date_time(self):
        print ("sudo date %T -s " +self.time[0]+self.sep+self.time[1]+self.sep+self.time[2])

    def action(self):
        self.set_date_time()
        
    def left(self):
        if self._mode == 0:
           super().left()  
        else:
           self.set_edit_mode(self._mode - 1)  

    def right(self):
        if self._mode < 2:
           self.set_edit_mode(self._mode + 1)  

    def show_state(self, draw, width, height):
        now = str(self.time[0]).zfill(2)+self.sep+str(self.time[1]).zfill(2)+self.sep+str(self.time[2]).zfill(2)

        gap = 6
        wu,hu = draw.textsize(text="\uf077", font=BaseState.font_awesome_small)
        wd,hd = draw.textsize(text="\uf078", font=BaseState.font_awesome_small)
        wt,ht = draw.textsize(text=now)

        top = height - ht - gap - hu
        left = (width - wt) / 2
        draw.text((left, top), text=now, fill = "yellow")

        ws,hs = draw.textsize(text=self.sep)
        wdd,hdd = draw.textsize(text="00")
        top = height - hd - gap - ht - gap - hu
        left = (width - wt) / 2 + (wdd - wu) / 2 + (ws + wdd) * self._mode           

        draw.text((left, top), text="\uf077", font=BaseState.font_awesome_small, fill="yellow")
        top += hu + gap + ht + gap          
        draw.text((left, top), text="\uf078", font=BaseState.font_awesome_small, fill="yellow")           
