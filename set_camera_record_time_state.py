from base_state import BaseState

class SetCameraRecordTimeState(BaseState):
    def __init__(self, home_state):
        super().__init__("set record time", " ", home_state, BaseState.font_awesome, BaseState.font_awesome_small)

    def up(self):
        BaseState.capture_duration += 1
        if BaseState.capture_duration > 99:
            BaseState.capture_duration = 10;

    def down(self):
        BaseState.capture_duration -= 1
        if BaseState.capture_duration < 10:
            BaseState.capture_duration = 99;

    def show_state(self, draw, width, height):
        # Record Time
        #    nnnn s
        duration = str(BaseState.capture_duration).zfill(2)

        gap = 6
        wh,hh = draw.textsize(text="Record Time")
        wu,hu = draw.textsize(text="\uf077", font=BaseState.font_awesome_small)
        wd,hd = draw.textsize(text="\uf078", font=BaseState.font_awesome_small)
        wt,ht = draw.textsize(text=duration)

        top = height - (hh + ht + hu + gap )
        left = (width - wh) / 2
        draw.text((left, top), text="Record Time", fill = "yellow")

        top += hh + gap
        left = (width - wt) / 2
        draw.text((left, top), text=duration, fill = "yellow")

        top -= hu/2
        left += wh + gap
        draw.text((left, top), text="\uf077", font=BaseState.font_awesome_small, fill="yellow")
        top += hu
        draw.text((left, top), text="\uf078", font=BaseState.font_awesome_small, fill="yellow")
