from datetime import datetime
from set_date_time_base import SetDateTimeBaseState
import os

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
        err = os.system("sudo date +%T -s " +str(self.time[0]).zfill(2)+self.sep+str(self.time[1]).zfill(2)+self.sep+str(self.time[2]).zfill(2))
        if err == 0:
            p = os.path.dirname(os.path.abspath(__file__))
            os.system("sudo "+p+"/writeTimeToRTC.sh")
