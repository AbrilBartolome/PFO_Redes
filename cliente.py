import socket

# ==============================
# Cliente TCP para enviar mensajes
# ==============================
def cliente():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("localhost", 5000))
        print("Conectado al servidor. Escriba 'exit' para salir.")

        while True:
            mensaje = input("Escribe un mensaje: ")
            cliente.send(mensaje.encode("utf-8"))
            if mensaje.lower() == "exit":
                break
            respuesta = cliente.recv(1024).decode("utf-8")
            print(f"Servidor: {respuesta}")

        cliente.close()
    except Exception as e:
        print(f"Error en el cliente: {e}")

if __name__ == "__main__":
    cliente()
