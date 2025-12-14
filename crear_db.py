# Este archivo se ejecuta una sola vez al inicio para crear la base
import sqlite3

conexion = sqlite3.connect('instituto.db')
cursor = conexion.cursor()
# Creamos la tabla solo si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INTEGER NOT NULL CHECK (edad >= 5 AND edad <= 120),
    curso TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE CHECK (email LIKE '%@%')
)
""")
conexion.commit()
conexion.close()
print("Base de datos y tabla 'alumnos' creada exitosamente.") 