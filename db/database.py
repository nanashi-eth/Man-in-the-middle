import sqlite3

class GameDatabase:
    def __init__(self, database_name='game_data.db'):
        try:
            self.connection = sqlite3.connect(database_name)
            self.cursor = self.connection.cursor()

            # Crear la tabla si no existe
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                                      last_score INTEGER, 
                                                                      best_score INTEGER)''')
            self.connection.commit()

            # Inicializar ambas puntuaciones a 0 si es la primera vez que se ejecuta
            self.cursor.execute('SELECT * FROM scores')
            if not self.cursor.fetchone():
                self.cursor.execute('INSERT INTO scores (last_score, best_score) VALUES (?, ?)', (0, 0))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def get_scores(self):
        try:
            self.cursor.execute('SELECT last_score, best_score FROM scores ORDER BY id DESC LIMIT 1')
            result = self.cursor.fetchone()
            if result:
                return result
            return 0, 0
        except sqlite3.Error as e:
            print(f"Error al obtener las puntuaciones: {e}")
            return 0, 0

    def update_scores(self, last_score, best_score):
        try:
            # Verificar si ya existen puntuaciones
            self.cursor.execute('SELECT * FROM scores')
            if self.cursor.fetchone():
                # Si existen, actualizar las puntuaciones
                self.cursor.execute('UPDATE scores SET last_score=?, best_score=? WHERE id=1',
                                    (last_score, best_score))
            else:
                # Si no existen, insertar nuevas puntuaciones
                self.cursor.execute('INSERT INTO scores (last_score, best_score) VALUES (?, ?)',
                                    (last_score, best_score))

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error al actualizar las puntuaciones: {e}")

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(f"Error al cerrar la conexión: {e}")
