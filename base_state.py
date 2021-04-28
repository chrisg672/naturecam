from luma.core.render import canvas
import logging
import os.path
import json

settings_file = "/home/pi/.nature_cam_settings.json"

class BaseState:
    def __init__(self, state_name, state_icon, home_state, font, font_small):
        self.update_required = True
        self.state_name = state_name
        self.state_icon = state_icon
        self.font = font
        self.font_small = font_small
        self.next_state = None
        self.prev_state = None
        if home_state == None:
            # Special case None => we are the home state
            self.home_state = self
            self.change_state(self)
        else:
            BaseState.home_state = home_state
        self.action_state = None
        self.parent_state = None
        BaseState.motion_was_detected = False


    def set_next_state(self, next_state):
        self.next_state = next_state
        if self.next_state != None:
            self.next_state.prev_state = self

    def set_action_state(self, action_state):
        self.action_state = action_state
        if self.action_state != None:
            self.action_state.parent_state = self

    def activate(self):
        self.update_required = True

    def should_update(self):
        return self.update_required

    def change_state(self, new_state):
        BaseState.current_state = new_state
        new_state.activate()

    def next(self):
        return self.next_state

    def prev(self):
        return self.prev_state

    def name(self):
        return self.state_name

    def icon(self):
        return self.state_icon

    def next_icon(self):
        if self.next_state != None:
            return self.next_state.icon()
        else:
            return " "

    def next_font(self):
        if self.next_state != None:
            return self.next_state.font_small
        else:
            return BaseState.font_awesome_small

    def prev_icon(self):
        if self.prev_state != None:
            return self.prev_state.icon()
        else:
            return " "

    def prev_font(self):
        if self.prev_state != None:
            return self.prev_state.font_small
        else:
            return BaseState.font_awesome_small

    def up(self):
        if self.prev() != None:
            self.change_state(self.prev())
        else:
            self.handleAnyInput()

    def down(self):
        if self.next() != None:
            self.change_state(self.next())
        else:
            self.handleAnyInput()

    def left(self):
        if self.parent_state != None:
            self.change_state(self.parent_state)
        else:
            self.handleAnyInput()

    def right(self):
        self.action()

    def action(self):
        if self.action_state != None:
            self.change_state(self.action_state)
        else:
            self.handleAnyInput()

    def home(self):
        self.change_state(BaseState.home_state)

    def handleAnyInput(self):
        return

    def motion_detected(self):
        BaseState.motion_was_detected = True

    def motion_stopped(self):
        BaseState.motion_was_detected = False

    def log_info(self, message):
        logging.info(message)

    def centre_text(self, draw, width, top, text):
        w, h = draw.textsize(text=text)
        left = (width - w) / 2
        draw.text((left, top), text=text, fill="yellow")

    def show_motion_dot(self, draw, width, height):
        if BaseState.motion_was_detected:
            draw.ellipse((width-4,0,width,4), fill="yellow")

    def show_state(self, draw, width, height):
        self.update_required = False
        gap = 3
        icon = self.icon()
        state = self.name()
        prev_icon = self.prev_icon()
        next_icon = self.next_icon()
        prev_font = self.prev_font()
        next_font = self.next_font()
        wp, hp = draw.textsize(text=prev_icon, font=prev_font)
        wi, hi = draw.textsize(text=icon, font=self.font)
        wa, ha = draw.textsize(text="\uf105", font=BaseState.font_awesome)
        ws, hs = draw.textsize(text=state)
        wn, hn = draw.textsize(text=next_icon, font=next_font)
        left = (width - wp) / 2
        top = 0
        draw.text((left, top), text=prev_icon, font=prev_font, fill="yellow")
        left = (width - wi) / 2
        top += hp + gap
        draw.text((left, top), text=icon, font=self.font, fill="yellow")
        if self.action_state != None:
            draw.text((width - wa, top), text="\uf105", font=BaseState.font_awesome, fill="yellow")
        if self.parent_state != None:
            draw.text((0, top), text="\uf104", font=BaseState.font_awesome, fill="yellow")
        left = (width - ws) / 2
        top += gap + hi
        draw.text((left, top), text=state, fill="yellow")
        left = (width - wn) / 2
        top += gap + hs
        draw.text((left, top), text=next_icon, font=next_font, fill="yellow")
        self.show_motion_dot(draw, width, height)

    def show(self, display):
        with canvas(display) as draw:
            self.show_state(draw, display.width, display.height)

    def is_running(self):
        return True

    def load_settings(self):
        if os.path.isfile(settings_file):
            with open(settings_file) as json_file:
                data = json.load(json_file)
                BaseState.capture_duration = data['capture_duration']
                BaseState.camera_mode = data['camera_mode']
    
    def save_settings(self):
        data = {}
        data['capture_duration'] = BaseState.capture_duration
        data['camera_mode'] = BaseSate.camera_mode
        with open(settings_file, 'w') as outfile:
            json.dump(data, outfile)

