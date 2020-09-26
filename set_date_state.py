from datetime import datetime
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

    def normalise(self):
        super().normalise()
        # Bug after 29 -> 28,29,28,29
        if not self.isValid():
            if self.time[1] == 2 and self.time[0] >= 29: # Febuary 29
                self.time[0] = 28
            elif self._mode == 1 and self.time[0] > 30: # Changing month
                self.time[0] = 30
            self.normalise()


    def set_date_time(self):
        print ("sudo date +%Y%m%d -s  20" +self.time[0]+self.time[1]+self.time[2])
