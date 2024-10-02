import socket
import threading
import os
import pickle

class Servidor():
    def __init__(self, host="localhost", port=7001):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        print(f"Servidor iniciado en {host}:{port}")
        print("Bienvenido al servidor de archivos.")
        print("Esperando conexiones...\n")

        self.clientes = []
        
        while True:
            conn, addr = self.sock.accept()
            print(f"Conexión aceptada de {addr}")
            self.clientes.append(conn)
            threading.Thread(target=self.procesar_conexion, args=(conn,)).start()
    
    def procesar_conexion(self, conn):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                command = pickle.loads(data)
                self.ejecutar_comando(command, conn)
            except Exception as e:
                print(f"Error: {e}")
                break
        conn.close()

    def ejecutar_comando(self, command, conn):
        if command == "lsFiles":
            response = self.listar_archivos()
            conn.send(pickle.dumps(response))
        elif command.startswith("get "):
            filename = command.split(" ")[1]
            self.enviar_archivo(filename, conn)
        elif command == "help":
            response = self.mostrar_ayuda()
            conn.send(pickle.dumps(response))
        else:
            response = "Comando no reconocido. Escriba 'help' para obtener la lista de comandos disponibles."
            conn.send(pickle.dumps(response))

    def listar_archivos(self):
        files = os.listdir("Files")
        return files

    def enviar_archivo(self, filename, conn):
        filepath = os.path.join("Files", filename)
        if os.path.isfile(filepath):
            # Enviar mensaje de inicio de transferencia
            conn.send(pickle.dumps("Inicio de la transferencia del archivo..."))
            
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            # Enviar el nombre del archivo y su contenido
            conn.send(pickle.dumps({"filename": filename, "data": file_data}))
        else:
            conn.send(pickle.dumps("Archivo no encontrado."))

    def mostrar_ayuda(self):
        ayuda = (
            "Comandos disponibles:\n"
            "1. lsFiles - Lista los archivos disponibles en el servidor.\n"
            "2. get <nombre_archivo> - Descarga el archivo especificado.\n"
            "3. help - Muestra este mensaje de ayuda.\n"
        )
        return ayuda

if __name__ == "__main__":
    server = Servidor()
