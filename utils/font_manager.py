# font_manager.py

from pyglet import font

# Rutas de archivos de fuentes
font_files = {
    'press_start_2p': 'assets/fonts/PressStart2P-Regular.ttf',
    'lcd_7': 'assets/fonts/LcdSolid.ttf',
    'c64_pro': 'assets/fonts/C64_Pro-STYLE.ttf',
    'minecraftia': 'assets/fonts/Minecraftia-Regular.ttf',
    'bitfont': 'assets/fonts/bitfont.ttf',
    'cascadia': 'assets/fonts/Cascadia.ttf'
}

# Nombres de fuentes
font_names = {
    'press_start_2p': 'Press Start 2P',
    'lcd_7': 'LCD Solid',
    'c64_pro': 'C64 Pro',
    'minecraftia': 'Minecraftia',
    'bitfont': 'BitFont',
    'cascadia': 'Cascadia Code'
}

# Diccionario para almacenar fuentes cargadas
loaded_fonts = {}

def load_font(font_name):
    global loaded_fonts

    # Verificar si la fuente ya ha sido cargada
    if font_name not in loaded_fonts:
        # Obtener la ruta del archivo de fuente desde el diccionario
        font_path = font_files.get(font_name)

        # Si no se encuentra la ruta del archivo, no hacer nada
        if not font_path:
            return

        # Cargar el archivo de fuente y obtener el objeto de fuente
        font.add_file(font_path)
        loaded_font = font.load(font_names.get(font_name))

        # Agregar la fuente al diccionario con la ruta y el indicador de carga
        loaded_fonts[font_name] = {'font': loaded_font, 'path': font_path}

