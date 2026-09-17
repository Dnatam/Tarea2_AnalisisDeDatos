# Implementación del pseudocódigo

# Verificar si un número es primo
def es_primo(numero):
    if numero < 2:
        return False

    divisor = 2

    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False

        divisor += 1

    return True


# Calcular el máximo común divisor
def calcular_mcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a


# Generador Blum Blum Shub
def bbs(p, q, semilla, n, k):
    valores_enteros = []
    valores_normalizados = []

    # Validar p
    if not es_primo(p) or p % 4 != 3:
        raise ValueError(
            "p debe ser primo y congruente con 3 módulo 4"
        )

    # Validar q
    if not es_primo(q) or q % 4 != 3 or q == p:
        raise ValueError(
            "q debe ser primo, distinto de p "
            "y congruente con 3 módulo 4"
        )

    M = p * q

    # Validar la semilla
    if (
        semilla == 0
        or semilla == 1
        or calcular_mcd(semilla, M) != 1
    ):
        raise ValueError(
            "La semilla debe ser distinta de 0 y 1 "
            "y coprima con M"
        )

    # Estado inicial
    X = (semilla**2) % M

    # Generar n números
    for i in range(n):
        R = 0

        # Construir R utilizando k bits
        for j in range(k):
            # Recurrencia BBS
            X = (X**2) % M

            # Extraer el bit menos significativo
            bit = X % 2

            # Agregar el bit al número R
            R = (R * 2) + bit

        # Normalización
        u = R / (2**k)

        # Guardar resultados
        valores_enteros.append(R)
        valores_normalizados.append(u)

    return valores_enteros, valores_normalizados

# Parámetros de BBS
p = 383
q = 503

# Semilla inicial
semilla = 8103

# Cantidad de valores a generar
n = 10000

# Cantidad de bits utilizados para formar cada número
k = 16


# Generar la secuencia
enteros, valores = bbs(p, q, semilla, n, k)

# Mostrar los primeros valores
print("Blum Blum Shub (BBS)\n")
print(f"p = {p}")
print(f"q = {q}")
print(f"M = {p * q}")
print(f"semilla = {semilla}")
print(f"k = {k}\n")
print("10 primeros valores generados")
for i in range(10):
    print(
        f"R{i + 1} = {enteros[i]} | "
        f"u{i + 1} = {valores[i]:.6f}"
    )