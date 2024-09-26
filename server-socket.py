import socket
import threading
import os
import pickle

class Servidor():
    def __init__(self, host="140.10.0.136", port=7000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        print(f"Servidor iniciado en {host}:{port}")
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
                response = self.ejecutar_comando(command)
                conn.send(pickle.dumps(response))
            except Exception as e:
                print(f"Error: {e}")
                break
        conn.close()

    def ejecutar_comando(self, command):
        if command == "lsFiles":
            return self.listar_archivos()
        elif command.startswith("get "):
            filename = command.split(" ")[1]
            return self.enviar_archivo(filename)
        else:
            return "Comando no reconocido."

    def listar_archivos(self):
        files = os.listdir("Files")
        return files

    def enviar_archivo(self, filename):
        filepath = os.path.join("Files", filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                file_data = f.read()
            return file_data
        else:
            return "Archivo no encontrado."

if __name__ == "__main__":
    server = Servidor()