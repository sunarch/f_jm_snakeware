"""Help browser for Snakeware"""

import os

import pygame
from pygame_gui.elements import UITextBox, UIWindow
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu


path = os.path.dirname(os.path.abspath(__file__))


def appname(x):
    """App name"""

    l = x.split("/")
    return l[-2]


def gethelp():
    """Get help"""

    d = path + "/../.."
    h = []
    for root, dirs, files in os.walk(d, topdown=False):
        for name in files:
            if "README" in name:
                h.append((appname(os.path.join(root, name)), os.path.join(root, name)))
    h.sort(key=lambda r: r[0])
    return h


class Help(UIWindow):
    """Help window"""

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (630, 490)),
            manager=manager,
            window_display_title="help",
            object_id="#help",
            resizable=False,
        )

        self.files = gethelp()
        self.last = self.files[0][0]

        self.menu = UIDropDownMenu(
            options_list=[p for p, q in self.files],
            starting_option=self.last,
            relative_rect=pygame.Rect(100, 0, 400, 30),
            manager=manager,
            container=self,
        )

        self.menu.current_state.should_transition = True

        self.textbox = UITextBox(
            "",
            relative_rect=pygame.Rect(0, 31, 600, 400),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )
        self.last = 0

    def process_event(self, event):
        """Process event"""

        super().process_event(event)

    def update(self, time_delta):
        """Update"""

        super().update(time_delta)

        n = self.menu.selected_option
        if n == self.last:
            return
        self.last = n
        s = ""
        for file_info in self.files:
            if file_info[0] == n:

                with open(file_info[1], encoding='UTF-8') as file:
                    for l in file:
                        x = l.strip()
                        if len(x) > 1 and x[0] == "#":
                            x = "<b><u>" + x[1:] + " </u></b>"
                        s += x + "<br>"

        self.set_text(s)

    def set_text(self, text):
        """Set text"""

        self.textbox.html_text = text
        self.textbox.rebuild()
