# code_npc.py
import pyglet
from utils.type_writter import TypewriterLabel
from utils.font_manager import load_font
from utils.color import hex_to_rgba
from utils.image_manager import get_image_manager_instance

# Cargar la fuente 'cascadia'
load_font('cascadia')

class NmapNpc:
    def __init__(self, console, font_size):
        # Inicialización de la clase NmapNpc
        self.x = 140
        self.y = 585
        
        # Configuración de la etiqueta de diálogo (TypewriterLabel)
        self.dialog_label = TypewriterLabel(text=console, 
                                            font_name="Cascadia Code",
                                            font_size=font_size,
                                            x=250, y=self.y + 47,
                                            width=400,
                                            anchor_x="center", anchor_y="center",
                                            color= hex_to_rgba("#39FF14"))
        self.dialog_label.original_text = console
        
        # Configuración de la animación del diálogo (monitor)
        image_manager = get_image_manager_instance()
        self.dialog_images = [
            image_manager.get_image('monitor'),
            image_manager.get_image('monitor_1')
        ]
        dialog_animation = pyglet.image.Animation.from_image_sequence(self.dialog_images, duration=0.5)
        self.dialog_sprite = pyglet.sprite.Sprite(dialog_animation, x=0 , y=self.y)
        
        # Configuración de la animación GIF del NPC
        self.animation = image_manager.get_image('code_npc')
        self.gif_sprite = pyglet.sprite.Sprite(self.animation, x=250, y=self.y + 80)
        self.configure_gif_sprite()

    def configure_gif_sprite(self):
        # Configurar el sprite GIF del NPC
        self.scaling_factor_y = 40 / self.gif_sprite.height
        self.scaling_factor_x = 40 / self.gif_sprite.width
        self.gif_sprite = pyglet.sprite.Sprite(self.animation, x=250, y=self.y + 80)
        self.gif_sprite.scale_y = self.scaling_factor_y
        self.gif_sprite.scale_x = self.scaling_factor_x
        self.gif_sprite.y -= self.gif_sprite.height // 2
        self.gif_sprite.x -= self.gif_sprite.width // 2

    def draw(self):
        # Dibujar el sprite del diálogo y el GIF en la pantalla
        self.dialog_sprite.scale_x = 500 / self.dialog_images[0].width 
        self.dialog_sprite.scale_y = 115 / self.dialog_images[0].height
        self.dialog_sprite.draw()
        self.gif_sprite.draw()
        self.dialog_label.draw()
        self.start_typewriting_animation()
        
    def start_typewriting_animation(self):
        # Iniciar la animación de la escritura en la etiqueta de diálogo
        pyglet.clock.schedule_interval(self.dialog_label.update_typewriter, 1/3)
