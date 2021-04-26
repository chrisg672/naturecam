from datetime import datetime
from base_state import BaseState
import subprocess

class AddWiFiNetwork(BaseState):
    def __init__(self, home_state):
        super().__init__("add wifi network", " ", home_state, BaseState.font_awesome, BaseState.font_awesome_small)

    def activate(self):
        self._available_ssids = []
        self._available_macs = []
        self._selected_network = 0
        self._state = "select"
        result = subprocess.run(["wpa_cli", "-i", "wlan0", "scan"], stdout=subprocess.PIPE)
        result = subprocess.run(["wpa_cli", "-i", "wlan0", "scan_results"], stdout=subprocess.PIPE)
        output = result.stdout.decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            tokens = line.split("\t")
            if len(tokens) > 4 and ("[WPS]" in tokens[3]):
                self._available_ssids.append(tokens[4])
                self._available_macs.append(tokens[0])
        super()

    def up(self):
        if (self._state == "select" and self._selected_network > 0):
            self._selected_network -= 1

    def down(self):
        if (self._state == "select" and self._selected_network < len(self._available_ssids)-1):
            self._selected_network += 1
    
    def action(self):
        self._state = "connect"

    def show_ssid(self, draw, num, top):
        if (top == 10):
            text = "> " + self._available_ssids[num]
        else:
            text = "  " + self._available_ssids[num]
        draw.text((15,top), text=text, fill="yellow")

    def show_connecting(self, draw, width, height):
        gap = 3
        wt,ht = draw.textsize(text="a")
        top = (height - 2*gap - 3*ht)/2
        self.centre_text(draw, width, top, "connecting...")
        top += gap + ht
        self.centre_text(draw, width, top, "push WPS button")
        top += gap + ht
        self.centre_text(draw, width, top, self._available_ssids[self._selected_network])

    def show_state(self, draw, width, height):
        if self._state == "connect":
            self.show_connecting(draw, width, height)
            result = subprocess.run(["wpa_cli", "-i", "wlan0", "wps_pbc", self._available_macs[self._selected_network]], stdout=subprocess.PIPE)
            output = result.stdout.decode("utf-8")
            self._result = output
            self._state = "result"
        elif self._state == "result":
            wt,ht = draw.textsize(text="a")
            top = (height - ht)/2
            self.centre_text(draw, width, top, self._result)
            if self._result == "OK":
                top += ht + gap
                self.centre_text(draw, width, top, "Reboot to connect to WiFi")
                top += ht + gap
                self.centre_text(draw, width, top, "(use witty-pi switch)")
        else:
            start = self._selected_network
            end = min(start + 5, len(self._available_ssids)-1)
            top = 10
            for i in range(start, end):
                self.show_ssid(draw, i, top)
                top += 12
