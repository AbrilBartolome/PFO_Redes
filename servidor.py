import socket
import sqlite3
import datetime

# ==============================
# Configuración de la base de datos
# ==============================
def inicializar_db():
    try:
        conn = sqlite3.connect("mensajes.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error al inicializar la DB: {e}")

# ==============================
# Guardar mensaje en la base de datos
# ==============================
def guardar_mensaje(contenido, ip_cliente):
    try:
        conn = sqlite3.connect("mensajes.db")
        cursor = conn.cursor()
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                       (contenido, fecha, ip_cliente))
        conn.commit()
        conn.close()
        return fecha
    except Exception as e:
        print(f"Error al guardar mensaje: {e}")
        return None

# ==============================
# Configuración del socket TCP/IP
# ==============================
def inicializar_socket():
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(("localhost", 5000))
        servidor.listen(5)
        print("Servidor escuchando en localhost:5000...")
        return servidor
    except Exception as e:
        print(f"Error al inicializar socket: {e}")
        exit(1)

# ==============================
# Aceptar conexiones y manejar mensajes
# ==============================
def manejar_conexiones(servidor):
    while True:
        conn, addr = servidor.accept()
        print(f"Conexión establecida con {addr}")
        while True:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            if data.lower() == "exit":
                print("Cliente desconectado.")
                break

            fecha = guardar_mensaje(data, addr[0])
            if fecha:
                respuesta = f"Mensaje recibido: {fecha}"
            else:
                respuesta = "Error al guardar el mensaje."
            conn.send(respuesta.encode("utf-8"))
        conn.close()

# ==============================
# Programa principal
# ==============================
if __name__ == "__main__":
    inicializar_db()
    servidor = inicializar_socket()
    manejar_conexiones(servidor)
