import random
import math

def es_primo (n):
  if n < 2:
    return False
  #for para comprobar si n es primo
  #si n es divisible por algun numero entre 1 y la raiz cuadrada de n, no es primo
  #n ** 0.5 es la raiz cuadrada de n

  for i in range (2, int(n ** 0.5) + 1): 
    if n % i == 0: 
      return False
  return True

def generar_primo(min, max):
  while True:
    p = random.randint(min, max)
    if es_primo(p):
      return p
    

def generar_claves():
  #1. Elegir dos primos q y p
  p = generar_primo(100, 500)
  q = generar_primo(100, 500)
  while p == q:
    q = generar_primo(100, 500)

  #2. Calcular n y phi(n)
  n = p * q
  phi = (p-1)*(q-1) 

  #3. Elegir e comprimo con phi(n)
  e = 65537
  if math.gcd(e, phi) != 1: #gcd(65537, 120)
    e = 3
    while math.gcd(e, phi) != 1:
      e += 2

  #4. calcular d = e^-1 mod phi(n)
  d = pow(e, -1, phi)

  #print("p = ", p)
  #print("q = ", q)
  print("n = ", n)
  #print("phi(n) = ", phi)
  print("e = ", e)
  print("d = ", d)

  #Devolvemos la calve privad y provada
  return (n, e), (n, d)

def cifra(mensaje, clave_publica):
  n, e = clave_publica
  #C = m^e mod n
  return [pow(ord (c), e, n) for c in mensaje]

def descifrar(cifrado, clave_privada):
    n, d = clave_privada
    
    #M = c^d (mod n)
    return "".join(chr(pow(c, d, n)) for c in cifrado)


if __name__ == "__main__":
    print("\nRSA Cifrado/Descifrado\n")
    while True:
        opcion = input("1. Cifrar\n2. Descifrar\nElige una opcion: ")
        if opcion == "1":
            print("\nGenerando claves...\n")
            public_key, private_key = generar_claves()
            print("Clave publica: ", public_key)
            print("Clave privada: ", private_key)
            mensaje = input("\nEscribe el mensaje a cifrar: ")
            cifrado = cifra(mensaje, public_key)
            print("\nMensaje cifrado: ", cifrado)
            break
        elif opcion == "2":
            n = int(input("\nIntroduce n de la clave privada: "))
            d = int(input("\nIntroduce d de la clave privada: "))
            private_key = (n, d)
            cifrado_input = input("\nIntroduce el mensaje cifrado (numeros separados por comas): ")
            cifrado = [int(x) for x in cifrado_input.split(",")]
            descifrado = descifrar(cifrado, private_key)
            print("\nMensaje descifrado: ", descifrado)
            break
        else:
            exit()