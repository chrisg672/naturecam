import datetime
from set_date_time_base import SetDateTimeBaseState

class SetDateState(SetDateTimeBaseState):
    def __init__(self, state_name, state_icon, home_state):
        self.min[0] = 0
        self.max[0] = 31
        self.min[1] = 1
        self.max[1] = 12
        self.min[2] = 2020
        self.max[2] = 2099
        self.sep = "/"
        super().__init__(state_name, state_icon, home_state)

    def set_date_time(self):
        print ("sudo date +%Y%m%d -s  " +self.time[0]+self.time[1]+self.time[2])