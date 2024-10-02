import socket
import threading
import sys
import os
import pickle

class Cliente():
    def __init__(self, host="localhost", port=7000):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(host), int(port)))
            msg_recv = threading.Thread(target=self.msg_recv)
            msg_recv.daemon = True 
            msg_recv.start()
            while True:
                msg = input('cliente> ')
                if msg != 'salir':
                    self.send_msg(msg)
                else:
                    self.sock.close()
                    sys.exit()
        except Exception as e:
            print("Error al conectar el socket:", e)
            
    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    data = pickle.loads(data)
                    if isinstance(data, bytes):  # Si se recibe un archivo
                        self.guardar_archivo(data)
                    else:
                        print(data)  # Imprimir la respuesta del servidor
            except Exception as e:
                print("Error en la recepción de datos:", e)
                break

    def send_msg(self, msg):
        try:
            self.sock.send(pickle.dumps(msg))
        except Exception as e:
            print('Error al enviar el mensaje:', e)

    def guardar_archivo(self, data):
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        filename = input("Nombre para guardar el archivo: ")
        with open(os.path.join("downloads", filename), 'wb') as f:
            f.write(data)
        print(f"Archivo guardado como {filename} en la carpeta 'downloads'.")

if __name__ == "__main__":
    cliente = Cliente()