from datetime import datetime
from set_date_time_base import SetDateTimeBaseState

class SetTimeState(SetDateTimeBaseState):
    def __init__(self, home_state):
        super().__init__("set time", home_state)
        self.min[0] = 0
        self.max[0] = 23
        self.min[1] = 0
        self.max[1] = 59
        self.min[2] = 0
        self.max[2] = 59
        self.sep = ":"

    def activate(self):
        now = datetime.now()
        self._mode = 0
        self.time = [int(now.strftime("%H")), int(now.strftime("%M")), int(now.strftime("%S"))]
        self.set_edit_mode(0)
        super()

    def set_date_time(self):
        print ("sudo date %T -s " +self.time[0]+self.sep+self.time[1]+self.sep+self.time[2])
