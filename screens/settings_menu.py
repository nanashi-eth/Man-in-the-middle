# settings_menu.py

import pyglet
from game.game_states import GameStates
from screens.hover_label import MyLabel
from utils.font_manager import load_font
from utils.image_manager import get_image_manager_instance
from utils.audio_manager import get_audio_manager_instance

# Cargar fuente, imágenes y sonido necesario
load_font('minecraftia')
image_manager = get_image_manager_instance()
click = get_audio_manager_instance().get_sound('menu')

class SettingsMenu:
    def __init__(self, game):
        # Inicializar el menú de configuración con el juego actual
        self.game = game
        self.batch = pyglet.graphics.Batch()
        self.labels = []  # Lista para almacenar las etiquetas de texto
        self.difficulty_functions = {
            1: self.set_easy_difficulty,
            2: self.set_medium_difficulty,
            3: self.set_hard_difficulty
        }
        self.create_labels()  # Crear las etiquetas del menú

    def create_labels(self):
        # Crear etiquetas para el título, dificultad actual y opciones de dificultad
        title_label = pyglet.text.Label(
            "Ajustes",
            font_name="Minecraftia",
            font_size=36,
            x=self.game.window_width // 2,
            y=3 * self.game.window_height // 4,
            anchor_x="center",
            anchor_y="top",
            batch=self.batch,
        )
        self.labels.append(title_label)

        difficulty_label = MyLabel(
            "",
            font_name="Minecraftia",
            font_size=24,
            x=self.game.window_width // 2,
            y=self.game.window_height // 2,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
        )
        self.labels.append(difficulty_label)

        easy_label = MyLabel(
            "Fácil",
            font_name="Minecraftia",
            font_size=18,
            x=self.game.window_width // 2,
            y=self.game.window_height // 2 - 50,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            callback=self.set_easy_difficulty
        )
        self.labels.append(easy_label)

        medium_label = MyLabel(
            "Medio",
            font_name="Minecraftia",
            font_size=18,
            x=self.game.window_width // 2,
            y=self.game.window_height // 2 - 100,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            callback=self.set_medium_difficulty
        )
        self.labels.append(medium_label)

        hard_label = MyLabel(
            "Difícil",
            font_name="Minecraftia",
            font_size=18,
            x=self.game.window_width // 2,
            y=self.game.window_height // 2 - 150,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            callback=self.set_hard_difficulty
        )
        self.labels.append(hard_label)
        self.labels[2].font_size = 24
        self.labels[2].hovered = True
        self.difficulty_functions[self.game.difficulty]()

        # Cargar el GIF para el fondo
        self.animation = image_manager.get_image('settings_gif')
        self.gif_sprite = pyglet.sprite.Sprite(self.animation)
        # Escalar el GIF para que ocupe toda la ventana
        self.scaling_factor_y = self.game.window_height / self.gif_sprite.height
        self.scaling_factor_x = self.game.window_width / self.gif_sprite.width
        self.gif_sprite = pyglet.sprite.Sprite(self.animation, x=0, y=0)
        self.gif_sprite.scale_y = self.scaling_factor_y
        self.gif_sprite.scale_x = self.scaling_factor_x

    def set_easy_difficulty(self):
        # Configurar la dificultad como fácil y actualizar la etiqueta
        self.game.difficulty = 1
        self.labels[1].text = f"Dificultad: {self.game.difficulty}"
        self.labels[1].color = (144, 238, 144, 255)

    def set_medium_difficulty(self):
        # Configurar la dificultad como media y actualizar la etiqueta
        self.game.difficulty = 2
        self.labels[1].text = f"Dificultad: {self.game.difficulty}"
        self.labels[1].color = (255, 255, 102, 255)

    def set_hard_difficulty(self):
        # Configurar la dificultad como difícil y actualizar la etiqueta
        self.game.difficulty = 3
        self.labels[1].text = f"Dificultad: {self.game.difficulty}"
        self.labels[1].color = (255, 102, 102, 255)

    def draw(self):
        # Dibujar el fondo y las etiquetas en la pantalla
        self.gif_sprite.draw()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        # Manejar eventos de teclado (Escape, flechas arriba/abajo)
        if symbol == pyglet.window.key.ESCAPE:
            self.game.state = GameStates.MAIN_MENU
        elif symbol == pyglet.window.key.UP:
            click.play()
            self.game.difficulty = max(self.game.difficulty - 1, 1)
            self.difficulty_functions[self.game.difficulty]()
            self.update_hover_label()  # Actualizar el hover del label
        elif symbol == pyglet.window.key.DOWN:
            click.play()
            self.game.difficulty = min(self.game.difficulty + 1, 3)
            self.difficulty_functions[self.game.difficulty]()
            self.update_hover_label()  # Actualizar el hover del label

    def reset_labels(self):
        # Reiniciar el estado de las etiquetas
        for label in self.labels[2:]:
            if isinstance(label, MyLabel):
                label.hovered = False
                label.font_size = 18

    def update_hover_label(self):
        # Actualizar el estado de hover de las etiquetas de dificultad
        for label in self.labels[2:]:
            if isinstance(label, MyLabel):
                difficulty_value = self.labels.index(label) - 1  # Índice de la dificultad en el rango [0, 2]
                label.hovered = (difficulty_value == self.game.difficulty)
                label.font_size = 24 if label.hovered else 18

    def on_mouse_press(self, x, y, button, modifiers):
        # Delegar el evento de clic del ratón a las etiquetas
        for label in self.labels:
            if isinstance(label, MyLabel):
                label.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        # Manejar eventos de movimiento del ratón para actualizar el hover
        for label in self.labels:
            if isinstance(label, MyLabel):
                label.update(x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # Manejar eventos de desplazamiento del ratón para cambiar la dificultad
        if self.labels[1].hovered:
            click.play()
            if scroll_y > 0:
                self.game.difficulty = max(self.game.difficulty - 1, 1)
                self.difficulty_functions[self.game.difficulty]()
            elif scroll_y < 0:
                self.game.difficulty = min(self.game.difficulty + 1, 3)
                self.difficulty_functions[self.game.difficulty]()
