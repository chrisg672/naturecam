import datetime
from set_date_time_base import SetDateTimeBaseState

class SetDateState(SetDateTimeBaseState):
    def __init__(self, home_state):
        super().__init__("aet date", home_state)
        self.min[0] = 0
        self.max[0] = 31
        self.min[1] = 1
        self.max[1] = 12
        self.min[2] = 20
        self.max[2] = 99
        self.sep = "/"

    def activate(self):
        now = datetime.datetime.now()
        self._mode = 0
        self.time = [now.strftime("%d"), now.strftime("%m"), now.strftime("%y")]
        self.set_edit_mode(0)
        super()

    def set_date_time(self):
        print ("sudo date +%Y%m%d -s  20" +self.time[0]+self.time[1]+self.time[2])
