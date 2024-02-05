# hover_label.py

import pyglet

class MyLabel(pyglet.text.Label):
    def __init__(self, *args, callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.hovered = False
        self.callback = callback

    def update(self, x, y):
        hover_x1 = self.x - self.content_width / 2
        hover_x2 = self.x + self.content_width / 2
        hover_y1 = self.y - self.content_height / 2
        hover_y2 = self.y + self.content_height / 2

        self.hovered = (hover_x1 < x < hover_x2 and hover_y1 < y < hover_y2)

        if self.hovered:
            self.font_size = 24
        else:
            self.font_size = 18

    def on_mouse_press(self, x, y, button, modifiers):
        if self.hovered and self.callback:
            self.callback()
