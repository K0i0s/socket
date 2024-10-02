import socket
import threading
import sys
import os
import pickle

class Cliente():
    def __init__(self, host="localhost", port=7001):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(host), int(port)))
            print("Conectado al servidor.")
            print("Bienvenido al cliente de archivos.")
            print("Escriba 'help' para obtener la lista de comandos.\n")
            
            self.prompt_ready = True  # Control para el prompt
            
            msg_recv = threading.Thread(target=self.msg_recv)
            msg_recv.daemon = True 
            msg_recv.start()

            while True:
                if self.prompt_ready:
                    msg = input('cliente> ')
                    if msg != 'salir':
                        self.send_msg(msg)
                    else:
                        self.sock.close()
                        sys.exit()
                else:
                    pass  # Evitar que el prompt se muestre mientras se reciben mensajes
        except Exception as e:
            print("Error al conectar el socket:", e)
            
    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    data = pickle.loads(data)
                    
                    # Deshabilitar el prompt hasta recibir todo el mensaje
                    self.prompt_ready = False
                    
                    if isinstance(data, list):  # Si es una lista (resultado de lsFiles)
                        print("Archivos disponibles:")
                        for file in data:
                            print(f"- {file}")
                    elif isinstance(data, dict):  # Si se recibe un archivo
                        self.guardar_archivo(data["filename"], data["data"])
                    else:
                        print(data)  # Imprimir cualquier otro tipo de mensaje del servidor
                    
                    # Asegurarse de que el cliente no esté enviando nada adicional
                    if not data:
                        continue

                    # Reactivar el prompt después de recibir el mensaje
                    self.prompt_ready = True
            except Exception as e:
                print("Error en la recepción de datos:", e)
                break

    def send_msg(self, msg):
        try:
            self.prompt_ready = False  # Desactivar el prompt hasta recibir respuesta
            self.sock.send(pickle.dumps(msg))
        except Exception as e:
            print('Error al enviar el mensaje:', e)

    def guardar_archivo(self, filename, data):
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        # Guardar el archivo con su nombre original
        with open(os.path.join("downloads", filename), 'wb') as f:
            f.write(data)
        print(f"Archivo '{filename}' guardado en la carpeta 'downloads'. Presione enter en caso de que esto aparezca como entrada del cliente")

if __name__ == "__main__":
    cliente = Cliente()
