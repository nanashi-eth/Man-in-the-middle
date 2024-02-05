import math
import random
from pyglet.text import Label
from utils.font_manager import load_font

# Cargar fuentes
load_font("press_start_2p")
load_font("press_start_2p")

class GameOverScreen:
    def __init__(self, window_width, window_height):
        # Inicialización de la pantalla de Game Over
        self.label = Label("Game Over", 
                           font_name="Press Start 2P",
                           x=window_width // 2, y=window_height // 2,
                           anchor_x="center", anchor_y="center", 
                           font_size=36, color=(255, 0, 0, 255))

        # Variables para la animación de sacudida/vibración
        self.vibration_duration = 0.0
        self.vibration_time = 0.0
        self.max_displacement = 10
        self.initial_position = (self.label.x, self.label.y)
        self.start_vibration(0.5)

    def draw(self):
        # Dibujar la pantalla de Game Over
        self.label.draw()

    def update(self, dt):
        # Actualizar la posición de la etiqueta en función de la vibración
        if self.vibration_duration > 0:
            # Calcula el desplazamiento propuesto
            dx = random.randint(-self.vibration_intensity, self.vibration_intensity)
            dy = random.randint(-self.vibration_intensity, self.vibration_intensity)
            
            # Limita el desplazamiento máximo
            dx = max(-self.max_displacement, min(self.max_displacement, dx))
            dy = max(-self.max_displacement, min(self.max_displacement, dy))

            self.label.x += dx
            self.label.y += dy
            self.vibration_duration -= dt
        else:
            # Restaura la posición inicial cuando la vibración ha terminado
            self.label.x, self.label.y = self.initial_position

    def start_vibration(self, duration):
        # Iniciar la animación de vibración
        self.vibration_duration = duration
        self.vibration_intensity = 5 

    def on_update(self, dt):
        # Llamar a la función de actualización en el ciclo de juego principal
        self.update(dt)
