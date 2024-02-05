# director.py

import pyglet
from pyglet.window import Window
from pyglet.gl import *
from pyglet.clock import schedule_interval, schedule_once
from game.game_states import GameStates
from screens.title_screen import MainMenu
from screens.settings_menu import SettingsMenu
from game.game import GameScreen
from screens.game_over import GameOverScreen
from db.database import GameDatabase
from enemies.npc import NPC
from utils.image_manager import get_image_manager_instance
from utils.audio_manager import get_audio_manager_instance

# Nueva constante para la duración de la pantalla de Game Over (en segundos)
GAME_OVER_SCREEN_DURATION = 4.0
audio_manager = get_audio_manager_instance()
background_music = audio_manager.get_sound('background_music')
coin = audio_manager.get_sound('coin')
game = audio_manager.get_sound('game')
_1 = audio_manager.get_sound('1')
_2 = audio_manager.get_sound('2')
_3 = audio_manager.get_sound('3')
class TitleScreen(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
        self.initialize_window()
        self.initialize_game_state()

    def initialize_window(self):
        display = pyglet.canvas.Display()
        screen = display.get_default_screen()
        self.set_location(screen.width // 2 - self.width // 2, 0)
        self.set_caption("Man-in-the-middle")
        self.cursor = pyglet.window.ImageMouseCursor(get_image_manager_instance().get_image('cursor'), 4, 32)
        self.set_mouse_cursor(self.cursor)
        self.set_icon(get_image_manager_instance().get_image('logo'))

        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Agregar la función de actualización al bucle de eventos
        schedule_interval(self.on_update, 1 / 60.0)

    def initialize_game_state(self):
        # Inicialización del estado del juego
        self.state = GameStates.MAIN_MENU
        self.window_width, self.window_height = self.width, self.height
        self.difficulty = 1
        self.best_score, self.last_score = 0, 0
        self.is_paused = False
        self.game_database = GameDatabase()
        self.player = pyglet.media.Player()
        self.sounds = pyglet.media.Player()
        self.player.queue(background_music)
        self.sounds.queue(coin)
        self.sounds.queue(game)
        self.sounds.loop = True
        # Cargar ambas puntuaciones desde la base de datos
        self.last_score, self.best_score = self.game_database.get_scores()

        # Crear instancias de menús
        self.main_menu = MainMenu(self.window_width, self.window_height)
        self.npc = NPC(x=110, y=10, batch=self.main_menu.batch1, batch1=self.main_menu.batch2)
        self.main_menu.best_score_label.text = f"Score: {self.best_score} (Best)"
        self.main_menu.score_label.text = f"Last score: {self.last_score}"
        self.settings_menu = SettingsMenu(self)
        self.game_screen = None
        self.game_over_screen = None

        # Cargar ambas puntuaciones desde la base de datos
        self.last_score, self.best_score = self.game_database.get_scores()

    def on_activate(self):
        # Manejar la activación de la ventana
        self.is_paused = False
        if self.state == GameStates.PLAYING:
            self.player.play()

    def on_deactivate(self):
        # Manejar la desactivación de la ventana
        self.is_paused = True
        if self.state == GameStates.PLAYING:
            self.player.pause()
    
    def on_key_press(self, symbol, modifiers):
        # Manejar la pulsación de teclas
        if self.state == GameStates.MAIN_MENU:
            if symbol == pyglet.window.key.ESCAPE or symbol == pyglet.window.key.ENTER:
                self.state = GameStates.SETTINGS
            elif symbol == pyglet.window.key.SPACE:
                self.sounds.play()
                schedule_once(self.play_music, 1.5)
        elif self.state == GameStates.SETTINGS:
            # Agrega lógica adicional para manejar teclas en el menú de ajustes
            self.settings_menu.on_key_press(symbol, modifiers)
        elif self.state == GameStates.PLAYING:
            self.game_screen.on_key_press(symbol, modifiers)
            
    def play_music(self, dt = None):
        # Reproducir la música y cambiar al estado de juego
        self.state = GameStates.PLAYING
        self.set_mouse_visible(False)
        self.game_screen = GameScreen(self.window_width, self.window_height, self.difficulty)
        self.sounds.pause()
        self.sounds.seek(0)
        self.player.play()
        self.player.loop = True
            
    def on_text(self, text):
        # Manejar la entrada de texto
        if self.state == GameStates.PLAYING:
            self.game_screen.on_text(text)

    def on_mouse_press(self, x, y, button, modifiers):
        # Manejar clics del ratón
            if self.state == GameStates.SETTINGS:
                self.settings_menu.on_mouse_press(x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # Manejar la rueda del ratón
        if self.state == GameStates.SETTINGS:
            self.settings_menu.on_mouse_scroll(x, y, scroll_x, scroll_y)
            
    def on_mouse_motion(self, x, y, dx, dy):
        # Manejar el movimiento del ratón
        if self.state == GameStates.SETTINGS:
            self.settings_menu.on_mouse_motion(x, y, dx, dy)
    


    def on_draw(self):
        # Manejar el dibujo en función del estado del juego
        self.clear()

        if self.state == GameStates.MAIN_MENU:
            # Dibujar el MainMenu
            self.main_menu.draw()
            self.npc.dialog_label_center.draw()
            self.npc.start_typewriting_animation()
        elif self.state == GameStates.SETTINGS:
            # Dibujar el SettingsMenu
            self.settings_menu.draw()
        elif self.state == GameStates.PLAYING:
            # Dibujar la pantalla de juego
            self.game_screen.draw()
        elif self.state == GameStates.GAME_OVER:
            # Dibuja la pantalla de Game Over
            self.game_over_screen.draw()
            self.last_score = self.game_screen.score
            if (self.last_score > self.best_score):
                self.best_score = self.last_score
                self.main_menu.best_score_label.text = f"Score: {self.best_score} (Best)"
            # Actualiza el label de puntaje en la pantalla de título
            self.main_menu.score_label.text = f"Last score: {self.last_score}"
        self.draw_window_border()
            
    def draw_window_border(self):
        # Configurar el color y ancho del borde
        border_color = (255, 255, 255, 255) 
        border_width = 3

        # Dibujar un rectángulo alrededor de la ventana (pegado al borde)
        pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
                             ('v2i', (border_width // 2, border_width // 2,
                                      self.width - border_width // 2, border_width // 2,
                                      self.width - border_width // 2, self.height - border_width // 2,
                                      border_width // 2, self.height - border_width // 2)),
                             ('c4B', border_color * 4))


    def on_update(self, dt):
        # Actualizar lógica del juego en función del estado
        if not self.is_paused:
            if self.state == GameStates.MAIN_MENU:
                self.main_menu.update_background(dt)
            elif self.state == GameStates.PLAYING:
                self.game_screen.on_update(dt)
                if self.game_screen.is_game_over():
                    self.handle_game_over_state()
                elif self.game_screen.exit:
                    self.return_to_main_menu_state()

            elif self.state == GameStates.GAME_OVER:
                self.game_over_screen.on_update(dt)

    def handle_game_over_state(self):
        # Manejar el estado de "Game Over"
        self.player.pause()
        self.player.seek(0)
        self.last_score = self.game_screen.score
        self.state = GameStates.GAME_OVER
        self.game_over_screen = GameOverScreen(self.window_width, self.window_height)
        schedule_once(self.return_to_main_menu_state, GAME_OVER_SCREEN_DURATION)
        if self.last_score > self.best_score:
            self.best_score = self.last_score
            self.main_menu.best_score_label.text = f"Score: {self.best_score} (Best)"
        if self.last_score < 15:
            _1.play()
        elif self.last_score < 30:
            _2.play()
        else:
            _3.play()
        self.main_menu.score_label.text = f"Last score: {self.last_score}"

    def return_to_main_menu_state(self, dt=None):
        # Volver al menú principal después del "Game Over"
        self.player.pause()
        self.player.seek(0)
        self.state = GameStates.MAIN_MENU
        self.set_mouse_visible(True)
        self.main_menu.score_label.text = f"Last score: {self.last_score}"

    def update_scores(self):
        # Actualizar las puntuaciones en la base de datos
        self.game_database.update_scores(self.last_score, self.best_score)

    def on_close(self):
        # Manejar el cierre de la ventana
        self.update_scores()
        self.game_database.close_connection()
        self.close()

if __name__ == "__main__":
    # Configurar y ejecutar la aplicación Pyglet
    config = pyglet.gl.Config(double_buffer=True)
    window = TitleScreen(width=500, height=700, config=config)
    window.push_handlers(on_activate=window.on_activate, on_deactivate=window.on_deactivate)
    pyglet.app.run()