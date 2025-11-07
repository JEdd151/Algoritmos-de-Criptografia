import time, os
from Crypto.PublicKey import RSA

###GENERACION DE CLAVES
def generar_claves(bits=1024):
    
    key = RSA.generate(bits)

    n, e, d = key.n, key.e, key.d
    
    with open("clave_publica.txt", "w") as pub:
        pub.write(f"{n},{e}")
    
    with open("clave_privada.txt", "w") as priv:
        priv.write(f"{n},{d}")
    
    return (n, e), (n, d)

####CIFRADO
def cifra(mensaje, clave_publica):
    n, e = clave_publica
    inicio = time.perf_counter()
    # Si es número, conviértelo a string
    if isinstance(mensaje, int):
        mensaje = str(mensaje)
    cifrado = [pow(ord(c), e, n) for c in mensaje]
    fin = time.perf_counter()
    with open("mensaje_cifrado.txt", "w") as f:
        f.write(",".join(map(str, cifrado)))
    return cifrado, fin - inicio

###DESCIFRADO
def descifrar(cifrado, clave_privada):
    n, d = clave_privada
    inicio = time.perf_counter()
    descifrado = "".join(chr(pow(c, d, n)) for c in cifrado)
    fin = time.perf_counter()
    return descifrado, fin - inicio

###PRUEBAS
def pruebas(archivo, clave_publica, clave_privada):
    with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
        contenido = f.read()

    tamaño_mb = os.path.getsize(archivo) / (1024 * 1024)

    ###cifra
    inicio_cif = time.perf_counter()
    cifrado, _ = cifra(contenido, clave_publica)
    fin_cif = time.perf_counter()

    ###descifra
    inicio_des = time.perf_counter()
    descifrado, _ = descifrar(cifrado, clave_privada)
    fin_des = time.perf_counter()


    tiempo_cif = fin_cif - inicio_cif
    tiempo_des = fin_des - inicio_des

    print("-" * 50)
    print(f"\nArchivo: {archivo}")
    print(f"Tamaño: {tamaño_mb:.2f} MB")
    print(f"Tiempo cifrado: {tiempo_cif:.4f} s")
    print(f"Tiempo descifrado: {tiempo_des:.4f} s")
    print("-" * 50)

    return tamaño_mb, tiempo_cif, tiempo_des

###MENU PRINCIPAL
def menu_principal():
    while True:
        opcion = input("RSA\n1. Cifrar\n2. Descifrar\n3. Pruebas\nElige una opción... ")

        if opcion == "1":
            print("\nGenerando claves...")
            public_key, private_key = generar_claves()
            print("Clave pública y privada guardadas en archivos.")

            mensaje = input("\nEscribe el mensaje o número a cifrar: ")
            cifrado, t1 = cifra(mensaje, public_key)
            print("\nMensaje cifrado guardado en 'mensaje_cifrado.txt'.")
            print(f"Tiempo de cifrado: {t1:.6f}s")

        elif opcion == "2":
            try:
                with open("clave_privada.txt", "r") as f:
                    n_str, d_str = f.read().strip().split(",")
                    private_key = (int(n_str), int(d_str))

                with open("mensaje_cifrado.txt", "r") as f:
                    cifrado = [int(x) for x in f.read().strip().split(",") if x]
                
                descifrado, t2 = descifrar(cifrado, private_key)
                print("\nMensaje descifrado:", descifrado)
                print(f"Tiempo de descifrado: {t2:.6f}s")
            
            except Exception as e:
                print("\nError al descifrar:", e)
        
        elif opcion == "3":
            pub, priv = generar_claves(1024)
            archivos = ["Archivos\\archivo_1mb.txt"] ##Modificar el archivo 
            resultados = []

            for archivo in archivos:
                resultados.append(pruebas(archivo, pub, priv))
            break
        else:
            break

if __name__ == "__main__":
    menu_principal()
