import datetime
from set_date_time_base import SetDateTimeBaseState

class SetTimeState(SetDateTimeBaseState):
    def __init__(self, state_name, state_icon, home_state):
        self.min[0] = 0
        self.max[0] = 23
        self.min[1] = 0
        self.max[1] = 59
        self.min[2] = 0
        self.max[2] = 59
        self.sep = ":"
        super().__init__(state_name, state_icon, home_state)

    def set_date_time(self):
        print ("sudo date %T -s " +self.time[0]+self.sep+self.time[1]+self.sep+self.time[2])
