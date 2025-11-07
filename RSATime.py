import random
import math
import time
import matplotlib.pyplot as plt  


def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generar_primo(min, max):
    while True:
        p = random.randint(min, max)
        if es_primo(p):
            return p


def generar_claves():
    p = generar_primo(100, 500)
    q = generar_primo(100, 500)
    while p == q:
        q = generar_primo(100, 500)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2

    d = pow(e, -1, phi)

    return (n, e), (n, d)


def cifra(mensaje, clave_publica):
    n, e = clave_publica
    inicio = time.perf_counter()
    cifrado = [pow(ord(c), e, n) for c in mensaje]
    fin = time.perf_counter()
    tiempo = fin - inicio
    return cifrado, tiempo


def descifrar(cifrado, clave_privada):
    n, d = clave_privada
    inicio = time.perf_counter()
    descifrado = "".join(chr(pow(c, d, n)) for c in cifrado)
    fin = time.perf_counter()
    tiempo = fin - inicio
    return descifrado, tiempo



def medir_tiempos(reps=5, show_plot=True):
    ##Mide tiempos de cifrado/descifrado para distintos tamaños de mensaje.
    ##reps: número de repeticiones por tamaño (se promedian los tiempos).
    ##show_plot: si True muestra la gráfica; si False sólo imprime los resultados.
    public_key, private_key = generar_claves()

    archivo = open ('Archivos/archivo_0mb.txt')
    print (archivo.readline(1))
    
    tiempos_cifrado = []
    tiempos_descifrado = []

    print("\n----- Medición de tiempos RSA (promedio de {} repeticiones) -----".format(reps))
    for t in tamanos:
        mensaje = "z" * t
        total_c = 0.0
        total_d = 0.0
        for _ in range(reps):
            cifrado, tiempo_c = cifra(mensaje, public_key)
            #descifrar devuelve (texto, tiempo)
            _, tiempo_d = descifrar(cifrado, private_key)
            total_c += tiempo_c
            total_d += tiempo_d

        prom_c = total_c / reps
        prom_d = total_d / reps
        tiempos_cifrado.append(prom_c)
        tiempos_descifrado.append(prom_d)
        print(f"Tamaño: {t:5d} | Cifrado promedio: {prom_c:.6f}s | Descifrado promedio: {prom_d:.6f}s")

    if show_plot:
        # Graficar resultados
        plt.figure(figsize=(8, 5))
        plt.plot(tamanos, tiempos_cifrado, marker='o', label='Cifrado')
        plt.plot(tamanos, tiempos_descifrado, marker='s', label='Descifrado')
        plt.xlabel("Tamaño del mensaje (caracteres)")
        plt.ylabel("Tiempo (segundos)")
        plt.title("Tiempos de cifrado y descifrado RSA")
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    while True:
        print("================================")
        print("\nRSA Cifrado/Descifrado con medición de tiempo\n")
        print("1. Cifrar mensaje (genera nuevas claves)")
        print("2. Descifrar mensaje (usando clave privada)")
        print("3. Medir tiempos con diferentes tamaños de entrada")
        print("4. Salir")
        opcion = input("\nElige una opción: ")

        if opcion == "1":
            public_key, private_key = generar_claves()
            print("\nClaves generadas:")
            print("Clave pública (n, e):", public_key)
            print("Clave privada (n, d):", private_key)

            mensaje = input("\nEscribe el mensaje a cifrar: ")
            cifrado, tiempo_c = cifra(mensaje, public_key)
            
            print(f"\nTiempo de cifrado: {tiempo_c:.6f} segundos")
            print("Mensaje cifrado:", cifrado)

        elif opcion == "2":
            try:
                print("\nIntroduce la clave privada:")
                n = int(input("Valor de n: "))
                d = int(input("Valor de d: "))
                private_key = (n, d)

                cifrado_input = input("\nIntroduce el mensaje cifrado (números separados por comas): ")
                cifrado = [int(x) for x in cifrado_input.split(",")]
                
                descifrado, tiempo_d = descifrar(cifrado, private_key)
                
                print(f"\nTiempo de descifrado: {tiempo_d:.6f} segundos")
                print("Mensaje descifrado:", descifrado)
            except ValueError:
                print("\nError: Asegúrate de introducir números válidos.")
            except Exception as e:
                print(f"\nError al descifrar: {str(e)}")

        elif opcion == "3":
            medir_tiempos()

        elif opcion == "4":
            break

        else:
            print("\nOpción inválida. Por favor, elige una opción válida.")