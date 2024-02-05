# game/game.py

from pyglet.text import Label
from pyglet.window import key
from pyglet.graphics import Batch
from pyglet.shapes import Line
from pyglet.clock import schedule_interval, schedule_once
from functools import wraps
from random import choice
from enemies.enemy import HexObject, TcpIpObject, hex_object_generator, bonus_object_generator
from enemies.npc import NPC
from utils.font_manager import load_font
from utils.image_manager import get_image_manager_instance
from utils.audio_manager import get_audio_manager_instance
import pyglet

# Cargar la fuente del juego
load_font("c64_pro")

# Obtener el sonido del bonus
bonus = get_audio_manager_instance().get_sound('bonus')

# Definir velocidades de caída para diferentes niveles de dificultad
difficulty_speeds = {
    1: 30,
    2: 45,
    3: 60,
}

# Duración del bonus (en segundos)
BONUS_DURATION = 12.0
BONUS_BLINK = 0.5
CODE_DURATION = 7.0

# Decorador para aumentar la puntuación
def increase_score(bonus=1):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.score += bonus
            self.update_score()
        return wrapper
    return decorator

class GameScreen:
    def __init__(self, window_width, window_height, difficulty):
        self.init_graphics(window_width, window_height)
        self.init_game_state(difficulty)
        self.init_schedule_callbacks(difficulty)

    def init_graphics(self, window_width, window_height):
        # Inicializar lotes gráficos para diferentes capas
        self.batch_labels = Batch()
        self.batch_back = Batch()
        self.batch_mid = Batch()
        self.batch_front = Batch()
        self.window_width = window_width
        self.window_height = window_height
        self.image_manager = get_image_manager_instance()

        # Inicializar etiquetas y elementos gráficos
        self.score_label = Label("0", x=25, y=50, anchor_x="left", font_name="C64 Pro", bold=True, anchor_y="center", batch=self.batch_back, font_size=20)
        self.ground_y = 100
        self.ground_line = Line(0, self.ground_y, window_width, self.ground_y, width=5, color=(255, 255, 255), batch=self.batch_labels)
        self.user_input_label = Label("", font_size=20, x=window_width // 2, y=self.ground_y - 50, anchor_x="center", font_name="C64 Pro", bold=True, anchor_y="center", batch=self.batch_back)
        self.bonus_label = Label("", x=window_width / 2, y=window_height - 57, anchor_x="center", font_name="Press Start 2P", bold=True, anchor_y="top", batch=self.batch_back, font_size=12)
        self.npc = NPC(x=50, y=10, batch=None, batch1=None)
        self.input_line = Line(150, 35, 350, 35, width=2, color=(255, 255, 255), batch=self.batch_back)

        # Inicializar sprite del personaje principal (PC)
        self.animation = self.image_manager.get_image('hacker')
        self.pc_1 = pyglet.sprite.Sprite(self.animation)
        self.scaling_factor_y = 80 / self.pc_1.height
        self.scaling_factor_x = 80 / self.pc_1.width
        self.pc_1 = pyglet.sprite.Sprite(self.animation, x=380, y=10, batch=self.batch_back)
        self.pc_1.scale_y = self.scaling_factor_y
        self.pc_1.scale_x = self.scaling_factor_x

        # Inicializar fondo del juego
        self.gif_sprite, self.background = self.load_background_images(window_height)

    def init_game_state(self, difficulty):
        # Inicializar el estado del juego
        self.score = 0
        self.user_input = ""
        self.bonus_time = False
        self.bonus_available = True
        self.bonus_blink_visible = True
        self.enemy_holder = []
        self.hex_generator = hex_object_generator(self, difficulty_speeds[difficulty])
        self.bonus_generator = bonus_object_generator(self)
        self.game_over = False
        self.exit = False

    def init_schedule_callbacks(self, difficulty):
        # Inicializar las funciones programadas (callbacks)
        schedule_interval(self.generate_enemy_callback, 60 / difficulty_speeds[difficulty])
        schedule_interval(self.update_bonus_status, 1.0)
        schedule_interval(self.toggle_bonus_label_visibility, BONUS_BLINK)

    def load_background_images(self, window_height):
        # Cargar imágenes de fondo
        animation = self.image_manager.get_image('game_gif')
        gif_sprite = pyglet.sprite.Sprite(animation, x=0, y=100, batch=self.batch_back)
        scaling_factor_y = (window_height - 200) / gif_sprite.height
        scaling_factor_x = self.window_width / gif_sprite.width
        gif_sprite.scale_y = scaling_factor_y
        gif_sprite.scale_x = scaling_factor_x

        back_image = self.image_manager.get_image('monitor')
        background = pyglet.sprite.Sprite(back_image, x=0, y=585)
        background.scale_x = 500 / back_image.width
        background.scale_y = 115 / back_image.height

        return gif_sprite, background

    def is_game_over(self):
        return self.game_over

    def draw(self):
        # Dibujar elementos en pantalla
        self.draw_enemies()
        self.draw_bonus_label()
        self.npc.sprite.draw()

    def draw_enemies(self):
        # Dibujar enemigos y elementos en capas
        self.batch_back.draw()
        self.batch_mid.draw()
        self.batch_front.draw()
        self.batch_labels.draw()
        self.background.draw()
        for enemy in self.enemy_holder:
            if isinstance(enemy, TcpIpObject):
                enemy.npc.draw()

    def draw_bonus_label(self):
        # Dibujar etiqueta de bonificación
        if self.bonus_time and self.bonus_blink_visible:
            self.bonus_label.text = "Bonus x 2"
            self.bonus_label.draw()
        else:
            self.bonus_label.text = ""

    def on_key_press(self, symbol, modifiers):
        # Manejar eventos de teclas presionadas
        if symbol == key.ENTER:
            self.check_answer()
            self.user_input = ""
            self.user_input_label.text = ""
        elif symbol == key.BACKSPACE:
            self.user_input = self.user_input[:-1]
            self.user_input_label.text = self.user_input
        elif symbol == key.ESCAPE:
            self.exit = True

    def toggle_bonus_label_visibility(self, dt):
        # Alternar visibilidad de la etiqueta de bonificación
        self.bonus_blink_visible = not self.bonus_blink_visible

    def on_text(self, text):
        # Manejar eventos de texto ingresado por el usuario
        if text.isdigit() and len(self.user_input) < 8:
            self.user_input += text
            self.user_input_label.text = self.user_input

    def update_user_input_label(self):
        # Actualizar etiqueta de entrada del usuario
        self.user_input_label.text = self.user_input

    def generate_enemy(self):
        # Generar un enemigo aleatorio
        if any(isinstance(enemy, TcpIpObject) for enemy in self.enemy_holder):
            self.bonus_available = False

        if self.bonus_available and not self.bonus_time:
            bonus_options = [next(self.hex_generator) for _ in range(4)]
            bonus_options.append(next(self.bonus_generator))
            return choice(bonus_options)
        else:
            return next(self.hex_generator)

    def generate_enemy_callback(self, dt):
        # Función de callback para generar enemigos
        new_enemy = self.generate_enemy()
        new_enemy.add_to_screen()
        self.enemy_holder.append(new_enemy)

        if isinstance(new_enemy, TcpIpObject):
            schedule_once(lambda dt: self.destroy_code_object(new_enemy, dt), CODE_DURATION)

    def destroy_code_object(self, code, dt):
        # Eliminar objeto de código después de cierto tiempo
        if code in self.enemy_holder:
            code.remove_self()

    def update_bonus_status(self, dt):
        # Actualizar estado de bonificación
        if not any(isinstance(enemy, TcpIpObject) for enemy in self.enemy_holder):
            self.bonus_available = True

    def on_update(self, dt):
        # Actualizar elementos en pantalla
        self.update_user_input_label()

        for enemy in self.enemy_holder:
            enemy.update(dt)
            if isinstance(enemy, HexObject) and enemy.package.y <= self.ground_y:
                self.game_over = True

    def check_answer(self):
        # Verificar respuestas del usuario
        for enemy in self.enemy_holder:
            if self.user_input.lower().replace(" ", "") == enemy.answer.lower():
                enemy.remove_self()
                if isinstance(enemy, HexObject):
                    if self.bonus_time:
                        self.puntuar_doble()
                    else:
                        self.puntuar()
                elif isinstance(enemy, TcpIpObject):
                    bonus.play()
                    self.bonus_time = True
                    schedule_once(self.reset_bonus_time, BONUS_DURATION)

    def reset_bonus_time(self, dt):
        # Reiniciar el tiempo de bonificación
        self.bonus_time = False
        self.bonus_blink_visible = True

    @increase_score()
    def puntuar(self):
        # Aumentar puntuación por respuesta correcta
        pass

    @increase_score(bonus=2)
    def puntuar_doble(self):
        # Aumentar puntuación por respuesta correcta con bonificación
        pass

    def update_score(self):
        # Actualizar etiqueta de puntuación
        self.score_label.text = f"{self.score}"
