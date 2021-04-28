from datetime import datetime
from set_date_time_base import SetDateTimeBaseState
import os

class SetDateState(SetDateTimeBaseState):
    def __init__(self, home_state):
        super().__init__("set date", home_state)
        self.min[0] = 1
        self.max[0] = 31
        self.min[1] = 1
        self.max[1] = 12
        self.min[2] = 20
        self.max[2] = 99
        self.sep = "/"

    def activate(self):
        now = datetime.now()
        self._mode = 0
        self.time = [int(now.strftime("%d")), int(now.strftime("%m")), int(now.strftime("%y"))]
        self.set_edit_mode(0)
        super()

    def isValid(self):
        format="%d/%m/%Y"
        date = str(self.time[0])+"/"+str(self.time[1])+"/20"+str(self.time[2])
        isValid = False
        try:
            datetime.strptime(date, format)
            isValid = True
        except ValueError:
            isValid = False
        return isValid

    def normalise(self, direction):
        super().normalise(direction)
        # Bug after 29 -> 28,29,28,29
        if not self.isValid():
            if self.time[1] == 2 and self.time[0] >= 29: # Febuary 29
                self.time[0] = 28
            elif self.time[0] > 30:
                if (direction < 0):
                    self.time[0] = 30
                else:
                    self.time[0] = 1
            self.normalise(direction)


    def set_date_time(self):
        err = os.system("sudo date +%Y%m%d -s  20" +str(self.time[2]).zfill(2)+str(self.time[1]).zfill(2)+str(self.time[0]).zfill(2))
        if err == 0:
            p = os.path.dirname(os.path.abspath(__file__))
            os.system("sudo "+p+"/writeTimeToRTC.sh")
