import socket ##conexion tcp/ip
import json
from Crypto.PublicKey import RSA
from Rsa import generar_claves, descifrar ##modulos


def enviar_con_longitud(sock, data: bytes):
  longitud = len(data).to_bytes(8, byteorder='big')
  sock.sendall(longitud + data)


def _recibir_exactamente(sock, n):
  datos = bytearray()
  while len(datos) < n:
    paquete = sock.recv(n - len(datos))
    if not paquete:
      raise ConnectionError("Conexión cerrada antes de recibir todos los datos")
    datos.extend(paquete)
  return bytes(datos)


def recibir_con_longitud(sock):
  longitud_bytes = _recibir_exactamente(sock, 8)
  longitud = int.from_bytes(longitud_bytes, byteorder='big')
  recibido = bytearray()
  while len(recibido) < longitud:
    paquete = sock.recv(min(65536, longitud - len(recibido)))
    if not paquete:
      raise ConnectionError("Conexión cerrada durante la recepción del mensaje")
    recibido.extend(paquete)
  return bytes(recibido)

def servidor():
  host = '127.0.0.1'
  port = 5000
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind ((host, port))
  server.listen(1)

  print(f"Servidor RSA escuchando en {host}:{port}.......")

  ##Generamos las claves
  pub, priv = generar_claves()
  print("Claves generadas y guardadas en archivos....")

  conn, addr = server.accept()
  print("Cliente conectado: ", addr)

  ##Enviar la calve al cliente
  conn.sendall(json.dumps(pub).encode())

  ##Recibe mensaje cifrado
  data = recibir_con_longitud(conn).decode()
  cifrado = json.loads(data)
  print("Mensaje cidrado recibido....")

  ##Descifrar mensaje
  mensaje, t = descifrar(cifrado, priv)
  print(f"Mensaje descifrado: {mensaje}") 
  print(f"Tiempo de descifrado: {t:.4f} s")

  ##retornar el mensaje cifrado
  enviar_con_longitud(conn, mensaje.encode())

  conn.close()
  server.close()

if __name__ == "__main__":
  servidor()