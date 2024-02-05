# enemies/npc.py
import pyglet
from pyglet.text import Label
from utils.image_manager import get_image_manager_instance
from utils.font_manager import load_font
from utils.type_writter import TypewriterLabel

# Cargar la fuente 'bitfont'
load_font("bitfont")

class NPC:
    def __init__(self, x, y, batch, batch1):
        # Inicialización de la clase NPC
        self.x = x
        self.y = y
        self.batch = batch
        self.batch1 = batch1
        self.image_manager = get_image_manager_instance()
        self.setup_sprite()
        self.setup_dialog()
        self.dialog_sprite.batch = batch
        self.sprite.batch = batch

    def setup_sprite(self):
        # Configuración del sprite animado del NPC
        sprite_sheet = self.image_manager.get_image('npc_sprite')
        image_grid = pyglet.image.ImageGrid(sprite_sheet, rows=1, columns=4)
        animation = pyglet.image.Animation.from_image_sequence(image_grid, duration=0.3)
        self.sprite = pyglet.sprite.Sprite(animation, x=self.x - 10, y=self.y - 5)

    def setup_dialog(self):
        # Configuración del diálogo y etiquetas del NPC
        padding = 5
        dialog_images = [
            self.image_manager.get_image('dialog_sprite_1'),
            self.image_manager.get_image('dialog_sprite_2')
        ]
        dialog_animation = pyglet.image.Animation.from_image_sequence(dialog_images, duration=0.5)
        self.dialog_sprite = pyglet.sprite.Sprite(dialog_animation, x=self.x, y=self.y - 10)
        self.dialog_sprite.scale_x = 300 / self.dialog_sprite.width
        self.dialog_sprite.scale_y = 130 / self.dialog_sprite.height

        self.label_top_y = self.dialog_sprite.y + 100
        self.label_center_y = self.dialog_sprite.y + 55
        intro = '''¡Bienvenido a "Man-in-the-Middle"! Sumérgete en el intrigante mundo del hacking mientras pones a prueba tus habilidades en binario, hexadecimal, direcciones IP y puertos.'''
        self.dialog_label_top = self.create_label("Mr.Robot", self.label_top_y)
        self.dialog_label_center = self.create_label(intro, self.label_center_y, multiline=True)
        self.dialog_label_center.original_text = intro

    def create_label(self, text, y, multiline=False):
        # Crear etiquetas de texto
        padding = 5
        if multiline:
            return TypewriterLabel(text=text, font_name="Bitfont", font_size=9, x=self.dialog_sprite.x + 85 + self.sprite.width,
                     y=y - 5, width=230 - 2 * padding, anchor_x='center', anchor_y='top' if not multiline else 'center', bold=True,
                     multiline=multiline, color=(255, 255, 255, 255))
        else:
            return Label(text, font_name="Bitfont", font_size=12, x=self.dialog_sprite.x + 150,
                     y=y + 13, width=280 - 2 * padding, anchor_x='center', anchor_y='top' if not multiline else 'center', bold=True,
                     multiline=multiline, color=(255, 255, 255, 255), batch=self.batch1)

    def start_typewriting_animation(self):
        # Iniciar la animación de escritura en la etiqueta de diálogo central
        pyglet.clock.schedule_interval(self.dialog_label_center.update_typewriter, 1/3)
