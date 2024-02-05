# enemies/enemy.py

import random
from pyglet.sprite import Sprite
from pyglet.text import Label
from random import choice, randint
import pyglet.shapes as shapes
from utils.font_manager import load_font
from enemies.nmap_npc import NmapNpc
from utils.color import hex_to_rgba
from utils.image_manager import get_image_manager_instance

# Cargar fuentes
load_font('lcd_7')

# Obtener instancia del gestor de imágenes
image_manager = get_image_manager_instance()
package_image = image_manager.get_image('package')

class Enemy:
    def __init__(self, game_screen, fall_speed=None, font_size=20, answer=None):
        # Inicialización de la clase Enemy
        self.fall_speed = fall_speed
        self.starting_x = randint(50, 750)
        self.starting_y = 580
        self.game_screen = game_screen
        self.font_size = font_size
        self.answer = answer
        self.npc = None

        self.label = Label(
            text="",
            font_name="LCD Solid",
            font_size=self.font_size,
            x=self.starting_x,
            y=self.starting_y,
            anchor_x="center",
            anchor_y="center",
            bold=True,
            batch=self.game_screen.batch_labels
        )

    def reset(self, value):
        # Reiniciar la posición y el valor del enemigo
        if isinstance(self, TcpIpObject):
            font_size = 13
            if self.type == 'IP':
                font_size = 11
            self.npc = NmapNpc(console=value, font_size=font_size)
            self.npc.draw()
        else:
            self.label.y = self.starting_y
            self.label.text = value

    def add_to_screen(self):
        # Añadir el enemigo a la pantalla
        self.reset()

    def update(self, dt):
        # Actualizar la posición del enemigo en la pantalla
        if isinstance(self, HexObject):
            self.label.y -= self.fall_speed * dt
            self.background.y -= self.fall_speed * dt
            self.package.y -= self.fall_speed * dt

    def remove_self(self):
        # Eliminar el enemigo de la pantalla
        self.label.delete()
        self.game_screen.enemy_holder.remove(self)

class HexObject(Enemy):
    def __init__(self, game_screen, fall_speed: float, *args, **kwargs):
        # Inicialización de la clase HexObject
        super().__init__(game_screen, fall_speed, *args, **kwargs)
        self.background = None
        self.label.color = hex_to_rgba('#39FF14')
        self.label.text = "00"
        self.draw_package()
        self.label.text = ""

    def reset(self):
        # Reiniciar la posición y el valor hexadecimal del HexObject
        hex_value = f"{randint(0, 255):02X}"
        binary_value = bin(int(hex_value, 16))[2:].zfill(8)
        super().reset(hex_value)
        self.answer = binary_value
        x = randint(self.label.content_width // 2, self.game_screen.window_width - self.label.content_width // 2)
        self.label.x = x
        self.package.x = self.label.x - self.label.content_width - 20
        self.background.x = self.label.x - self.label.content_width // 2 - 2

    def draw_package(self):
        # Dibujar el paquete en la pantalla
        package_y = self.starting_y - 20

        self.package = Sprite(package_image, x=0, y=package_y)
        self.package.scale = 135 / package_image.height
        self.background = shapes.Rectangle(x=0,
            y=self.label.y - self.label.content_height // 2 - 2,
            width=self.label.content_width + 4,
            height=self.label.content_height + 4,
            color=(0, 0, 0), batch=self.game_screen.batch_front)
        self.background.opacity = 192
        self.package.batch = self.game_screen.batch_mid

def hex_object_generator(game_screen, fall_speed: float):
    # Generador de objetos HexObject
    while True:
        yield HexObject(game_screen, fall_speed, answer="")

class TcpIpObject(Enemy):
    def __init__(self, game_screen, *args, **kwargs):
        # Inicialización de la clase TcpIpObject
        super().__init__(game_screen, *args, **kwargs)
        self.starting_y = 680
        self.type = None
        self.text = ''

    def generate_block(self):
        # Generar un bloque con información IP o de servicio
        service_dict = {
            "http": '80',
            "https": '443',
            "ftp": '21',
            "ssh": '22',
            "telnet": '23',
        }
        block_type = choice(["IP", "Service"])
        self.type = block_type

        if block_type == "IP":
            ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            mask = random.randint(24, 32)
            self.answer = f"{self.count_devices(ip, mask)}"
            self.text = f"[root@mr.robot]# nmap -sL {ip}/{mask}"
        elif block_type == "Service":
            service_name = choice(list(service_dict.keys()))
            self.answer = service_dict[service_name]
            self.text = f"SERVICE:{service_name.upper()} - STATE:{choice(['open', 'closed']).upper()}"
        else:
            raise ValueError("Tipo de bloque no válido")

    def count_devices(self, ip, mask):
        # Contar dispositivos en una red con una máscara dada
        return 2**(32 - mask) - 2

    def reset(self):
        # Reiniciar la posición y la información del TcpIpObject
        self.generate_block()
        super().reset(self.text)

    def generate_random_ip(self):
        # Generar una dirección IP aleatoria
        return ".".join(str(randint(0, 255)) for _ in range(4))

def bonus_object_generator(game_screen):
    # Generador de objetos TcpIpObject (objetos de bonificación)
    while True:
        yield TcpIpObject(game_screen, answer="")
