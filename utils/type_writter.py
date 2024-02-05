# type_writter.py

import pyglet

class TypewriterLabel(pyglet.text.Label):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.visible_characters = 0
        self.time_per_character = 0.05  # Tiempo ajustado por carácter (ajustar según sea necesario)
        self.elapsed_time = 0

    def draw(self):
        displayed_text = self.text[:self.visible_characters]
        self.text = displayed_text
        super().draw()
        self.text = self.original_text  # Restaurar el texto original después de dibujar

    def update_typewriter(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.time_per_character:
            self.visible_characters += 1
            self.elapsed_time = 0
