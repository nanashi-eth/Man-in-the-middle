# title_screen.py

import pyglet
from pyglet.text import Label
from pyglet.graphics import Batch
from pyglet.image import load
from utils.font_manager import load_font
from utils.image_manager import get_image_manager_instance
from utils.audio_manager import get_audio_manager_instance

load_font("press_start_2p")
load_font("bitfont")
image_manager = get_image_manager_instance()
start = get_audio_manager_instance().get_sound('start')

class MainMenu:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.batch = Batch()
        self.batch1 = Batch()
        self.batch2 = Batch()
        

        self.main_menu_label_1 = Label(text="Man-in-the-middle", font_name="Press Start 2P", x=window_width // 2, y=window_height // 2, anchor_x="center", font_size=20, batch=self.batch1)
        self.main_menu_label_2 = Label(text="Insert Bitcoin and Press [Space] to Start or [Escape] to go to settings", x=window_width // 2 , y=window_height // 2 - 30, anchor_x="center", anchor_y="top", font_size=12, multiline=True, width=window_width // 2 + 50, bold=True, batch=self.batch1)
        
        self.score_label = Label("", x=10, y=self.window_height - 20, font_name="BitFont", anchor_x="left", anchor_y="center", font_size=16, bold=True, color=(255, 255, 255, 255), batch=self.batch1)
        self.best_score_label = Label("", x=10 , y=self.window_height - 50, font_name="BitFont", bold=True, anchor_x="left", anchor_y="center", font_size=16, color=(255, 255, 255, 255), batch=self.batch1)

        # Cargar la imagen de fondo
        self.background_image = image_manager.get_image('background') 

        # Configurar la animación de parallax
        self.parallax_speed = 200
        self.background_sprite_1 = pyglet.sprite.Sprite(self.background_image)
        self.background_sprite_2 = pyglet.sprite.Sprite(self.background_image)
        self.background_sprite_2.y = window_height
        
        self.animation = image_manager.get_image('coin')
        self.gif_sprite = pyglet.sprite.Sprite(self.animation)
        # Escalar el GIF para que ocupe toda la altura de la ventana
        self.scaling_factor_y = 40 / self.gif_sprite.height
        self.scaling_factor_x = 40 / self.gif_sprite.width
        self.gif_sprite = pyglet.sprite.Sprite(self.animation, x=self.window_width // 2 - 20, y=245)
        self.gif_sprite.scale_y = self.scaling_factor_y
        self.gif_sprite.scale_x = self.scaling_factor_x
        self.background_sprite_1.batch = self.batch
        self.background_sprite_2.batch = self.batch
        start.play()

    def draw(self):
        # Dibujar las imágenes de fondo y labels
        self.batch.draw()
        self.gif_sprite.draw()
        self.batch1.draw()
        self.batch2.draw()

    def update_background(self, dt):
        # Actualizar la posición de las imágenes para el efecto parallax
        self.background_sprite_1.y -= self.parallax_speed * dt
        self.background_sprite_2.y -= self.parallax_speed * dt

        # Reposicionar las imágenes cuando alcancen el final de la ventana
        if self.background_sprite_1.y <= -self.window_height:
            self.background_sprite_1.y = self.background_sprite_2.y + self.window_height

        if self.background_sprite_2.y <= -self.window_height:
            self.background_sprite_2.y = self.background_sprite_1.y + self.window_height
