import sqlite3
from colorama import Fore, init
# Inicializamos colorama para usar colores en consola
init(autoreset=True)

#Función para conectar a la base de datos
def conectar():
    return sqlite3.connect("instituto.db")

#Funciones CRUD
def agregar_alumno():
    # Pedimos y validamos los datos
    nombre = input("Nombre: ").strip().capitalize()
    apellido = input("Apellido: ").strip().capitalize()
    edad = input("Edad: ").strip()
    curso = input("Curso: ").strip().upper()
    email = input("Email: ").strip().lower()
# Validaciones básicas
    if not nombre or not apellido or not edad or not curso or not email:
        print(Fore.RED + "Todos los campos son obligatorios.")
        return

    if not edad.isdigit() or not (5 <= int(edad) <= 120):
        print(Fore.RED + "La edad debe ser un número entre 5 y 120.")
        return

    if "@" not in email:
        print(Fore.RED + "El email debe contener '@'(ejemplo@correo.com).")
        return

    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute("INSERT INTO alumnos (nombre, apellido, edad, curso, email) VALUES (?, ?, ?, ?, ?)",
                       (nombre, apellido, int(edad), curso, email))
        con.commit()
        print(Fore.GREEN + "Alumno agregado correctamente.")
    except sqlite3.IntegrityError:
        print(Fore.RED + "Error: El email ya está registrado.")
    finally:
        con.close()
def consultar_alumnos():
    con = conectar()
    cursor = con.cursor()
    print("1. Ver todos los alumnos")
    print("2. Buscar por nombre")

    opcion = input("Opción: ")
    if opcion == "1":
        cursor.execute("SELECT * FROM alumnos")
    elif opcion == "2":
        nombre = input("Ingrese el nombre a buscar: ")
        cursor.execute("SELECT * FROM alumnos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    else:
        print(Fore.RED + "Opción inválida")
        con.close()
        return

    alumnos = cursor.fetchall()
    if alumnos:
        for a in alumnos:
            print(Fore.CYAN + f"{a[0]} | {a[1]} {a[2]} | Edad: {a[3]} | Curso: {a[4]} | Email: {a[5]}")
    else:
        print(Fore.YELLOW + "No se encontraron alumnos.")
    con.close()

# =================================
def eliminar_alumno():
    con = conectar()
    cursor = con.cursor()
    consultar_alumnos()
    id_eliminar = input("Ingrese el ID del alumno a eliminar: ")
    confirmacion = input(f"¿Está seguro que desea eliminar al alumno con ID {id_eliminar}? (s/n): ")

    if confirmacion.lower() == "s":
        cursor.execute("DELETE FROM alumnos WHERE id = ?", (id_eliminar,))
        con.commit()
        print(Fore.GREEN + "Alumno eliminado.")
    else:
        print(Fore.YELLOW + "Operación cancelada.")
    con.close()

# =================================
def menu():
    while True:
        print("\n" + Fore.BLUE + "=== MENÚ PRINCIPAL ===")
        print("1. Registrar alumno")
        print("2. Consultar alumnos")
        print("3. Eliminar alumno")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_alumno()
        elif opcion == "2":
            consultar_alumnos()
        elif opcion == "3":
            eliminar_alumno()
        elif opcion == "4":
            print(Fore.MAGENTA + "¡Hasta luego!")
            break
        else:
            print(Fore.RED + "Opción inválida.")

# Ejecutamos el menú principal
menu()      