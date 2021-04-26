
from base_state import BaseState

class SetCameraModeState(BaseState):
    def __init__(self, home_state):
        super().__init__("set camera", " ", home_state, BaseState.font_awesome, BaseState.font_awesome_small)

    def up(self):
        if BaseState.camera_mode > 0:
            BaseState.camera_mode -= 1

    def down(self):
        if BaseState.camera_mode < 2:
            BaseState.camera_mode += 1

    def action(self):
        super().left()

    def show_state(self, draw, width, height):
        icon = "\uf185" # Sun
        text = "Day Mode"
        if BaseState.camera_mode == 2:
            # Auto Mode
            icon = "\uf0d0" # Magic Wand
            text = "Auto Mode"
        elif BaseState.camera_mode == 1:
            # Night Mode
            icon = "\uf186" # Moon
            text = "Night Mode"
        gap = 3
        wp, hp = draw.textsize(text=icon, font=BaseState.font_awesome_small)
        wi, hi = draw.textsize(text=icon, font=BaseState.font_awesome)
        ws, hs = draw.textsize(text=text)
        left = (width - wi) / 2
        top = hp + gap
        draw.text((left, top), text=icon, font=self.font, fill="yellow")
        left = (width - ws) / 2
        top += gap + hi
        draw.text((left, top), text=text, fill="yellow")
        self.show_motion_dot(draw, width, height)
