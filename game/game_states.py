from enum import Enum

class GameStates(Enum):
    MAIN_MENU = 0
    SETTINGS = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    TOP_SCORES = 5