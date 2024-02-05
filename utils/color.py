# utils/color.py
def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    value = int(hex_color, 16)
    
    # Extraer componentes de color
    red = (value >> 16) & 0xFF
    green = (value >> 8) & 0xFF
    blue = value & 0xFF
    
    # Extraer valor alfa (opacidad)
    alpha = value >> 24 if len(hex_color) == 8 else 255  # Tomar los últimos 8 bits
    
    return red, green, blue, alpha



