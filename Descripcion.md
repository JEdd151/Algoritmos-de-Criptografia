

## RSA

Es un sistema de criptografía de clave pública (o asimétrica), lo que significa que utiliza un par de claves diferentes para cifrar y descifrar:

- Una clave pública para el cifrado (que se puede compartir) 
- Y una clave privada para el descifrado (que debe mantenerse en secreto).

Su seguridad se basa en la difucultad de factorizar números enteror grandes en sus factores primos.

### Funcionamiento

El proceso de RSA consta de tres pasos:

1. Generación de Claves.
   
    Se genera la clave pública y privada a partir de dos números primos grandes (*p* y *q*), elegidos al azar y mantenidos en secreto.

    - Se calcula el módulo *n = p x q*. La longitud de la clave es la longitud de bits de *n*.
    - Se elige un exponente de cifrado *e*, un número pequeño coprimo con *(p-1)(q-1)*.
    - Se calcula el exponente de descifrad *d*, que es el inverso multiplicativo de *e* módulo *(p-1)(q-1)*.
    - Clave pública: es el par *(e, n)*, y se hace pública.
    - Clave privada: Es par *(d, n)*, y se mantiene en secreto. Los números *p, q* y *(p-1)(q-1)* se descartan.
 
2. Cifrado.
3. Descifrado.