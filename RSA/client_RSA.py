import socket
import json
from Rsa import cifra


def enviar_con_longitud(sock, data: bytes):
  longitud = len(data).to_bytes(8, byteorder='big')
  sock.sendall(longitud + data)


def recibir_con_longitud(sock):
  longitud_bytes = sock.recv(8)
  if len(longitud_bytes) < 8:
    raise ConnectionError("No se pudo leer la longitud del mensaje")
  longitud = int.from_bytes(longitud_bytes, byteorder='big')

  recibido = bytearray()
  while len(recibido) < longitud:
    paquete = sock.recv(min(65536, longitud - len(recibido)))
    if not paquete:
      raise ConnectionError("Conexión cerrada mientras se recibía la respuesta")
    recibido.extend(paquete)
  return bytes(recibido)

def cliente():
  host = '127.0.0.1'
  port = 5000

  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((host, port))

  ##recibe la clave pública del servidor
  pub_data = client.recv(8192).decode()
  pub = tuple(json.loads(pub_data))
  print("Clave pública recibida....")

  ##enviar mensaje cifrado
  opcion = input("1. Escribir mensaje manualmente\n2. Cargar mensaje desde archivo\nElige una opción: ")

  if opcion == "2":
    ruta = input("Ruta del archivo a enviar: ")
    try:
      with open(ruta, "r", encoding="utf-8", errors="ignore") as archivo:
        mensaje = archivo.read()
      print(f"Archivo '{ruta}' cargado correctamente ({len(mensaje)} caracteres).")
    except FileNotFoundError:
      print("Archivo no encontrado. Saliendo...")
      client.close()
      return
    except Exception as e:
      print(f"Error al leer el archivo: {e}")
      client.close()
      return
  else:
    mensaje = input("Escribe el mensaje a enviar: ")

  cifrado, t = cifra(mensaje, pub)
  print(f"Mensaje cifrado en {t:.4} s")

  enviar_con_longitud(client, json.dumps(cifrado).encode())

  ##espera la respuesta del servidor
  respuesta = recibir_con_longitud(client).decode()
  print("Servidor respondio con: ", respuesta)

  client.close()

if __name__ == "__main__":
  cliente()