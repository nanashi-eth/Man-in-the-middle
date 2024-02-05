# audio_manager.py

import pyglet

class AudioManager:
    _instance = None
    audio_paths = {
        'coin': 'assets/audio/coin.wav',
        'background_music': 'assets/audio/music.mp3',
        'game': 'assets/audio/game_start.wav',
        'start': 'assets/audio/start.wav',
        'menu': 'assets/audio/click.wav',
        'bonus': 'assets/audio/finish_him.wav',
        '1': 'assets/audio/1.wav',
        '2': 'assets/audio/2.mp3',
        '3': 'assets/audio/3.wav',
    }

    def __new__(cls, *args, **kwargs):
        # Implementar el patrón Singleton para AudioManager
        if not cls._instance:
            cls._instance = super(AudioManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.sounds = {}
            cls._instance.loaded_paths = set()
        return cls._instance

    @classmethod
    def load_sound(cls, name, path):
        # Cargar un sonido en la instancia AudioManager
        cls._instance.loaded_paths.add(path)
        cls._instance.sounds[name] = pyglet.resource.media(path, streaming=False)

    @classmethod
    def get_sound(cls, name):
        # Obtener un sonido de la instancia AudioManager, cargándolo si es necesario
        if name not in cls._instance.sounds:
            path = cls.audio_paths.get(name)
            if path:
                cls.load_resource(name, path)
        return cls._instance.sounds.get(name)

    @classmethod
    def load_resource(cls, name, path):
        # Cargar un recurso de audio en la instancia AudioManager
        extension = path.split('.')[-1].lower()
        if extension in ('wav', 'mp3', 'ogg'):
            cls.load_sound(name, path)

def get_audio_manager_instance():
    # Obtener una instancia única de AudioManager
    return AudioManager()
