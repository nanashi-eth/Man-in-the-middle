# image_manager.py

import pyglet

class ImageManager:
    _instance = None

    # Rutas de archivos de imágenes
    image_paths = {
        'cursor': 'assets/images/cursor.png',
        'logo': 'assets/images/logo.png',
        'background': 'assets/images/matrixhex.png',
        'settings_gif': 'assets/images/settings.gif',
        'game_gif': 'assets/images/background.gif',
        'npc_sprite': 'assets/images/npc_sprite.png',
        'code_npc': 'assets/images/code_npc_sprite.gif',
        'dialog_sprite_1': 'assets/images/dialog_sprite_1.png',
        'dialog_sprite_2': 'assets/images/dialog_sprite_2.png',
        'monitor': 'assets/images/monitor.png',
        'monitor_1': 'assets/images/monitor_1.png',
        'package': 'assets/images/package.png',
        'coin': 'assets/images/coin.gif',
        'hacker': 'assets/images/hacker.gif',
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.images = {}
            cls._instance.loaded_paths = set()
        return cls._instance

    @classmethod
    def load_image(cls, name, path):
        # Agregar la ruta del archivo a las rutas cargadas
        cls._instance.loaded_paths.add(path)
        # Cargar la imagen y agregarla al diccionario de imágenes
        cls._instance.images[name] = pyglet.resource.image(path)

    @classmethod
    def load_animation(cls, name, path):
        # Agregar la ruta del archivo a las rutas cargadas
        cls._instance.loaded_paths.add(path)
        # Cargar la animación y agregarla al diccionario de imágenes
        cls._instance.images[name] = pyglet.image.load_animation(path)

    @classmethod
    def get_image(cls, name):
        if name not in cls._instance.images:
            path = cls.image_paths.get(name)
            if path:
                cls.load_resource(name, path)
        return cls._instance.images.get(name)

    @classmethod
    def load_resource(cls, name, path):
        # Obtener la extensión del archivo
        extension = path.split('.')[-1].lower()
        # Determinar cómo cargar el recurso según la extensión
        if extension == 'gif':
            cls.load_animation(name, path)
        elif extension in ('png', 'jpg', 'jpeg', 'bmp'):
            cls.load_image(name, path)

def get_image_manager_instance():
    return ImageManager()
