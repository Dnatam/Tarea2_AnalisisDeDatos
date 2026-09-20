import random
import math
import statistics

# Implementación propia de MT19937
def mt19937(n, semilla):
    valores_enteros = []
    valores_normalizados = []

    # Vector de estado interno de 624 palabras
    estado = [0] * 624
    estado[0] = semilla

    for i in range(1, 624):
        estado[i] = (
            1812433253
            * (estado[i - 1] ^ (estado[i - 1] >> 30))
            + i
        ) % (2**32)

    # Generar n valores
    for k in range(n):
        y = (
            (estado[k % 624] & 0x80000000)
            | (estado[(k + 1) % 624] & 0x7FFFFFFF)
        )

        # Aplicar la transformación twist
        if (y & 1) == 0:
            x = y >> 1
        else:
            x = (y >> 1) ^ 0x9908B0DF

        estado[k % 624] = (
            estado[(k + 397) % 624] ^ x
        )

        y = estado[k % 624]

        # Tempering
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9D2C5680)
        y = y ^ ((y << 15) & 0xEFC60000)
        y = y ^ (y >> 18)

        # Mantener el resultado en 32 bits
        y = y & 0xFFFFFFFF

        # Normalización al intervalo [0, 1)
        r = y / (2**32)

        valores_enteros.append(y)
        valores_normalizados.append(r)

    return valores_enteros, valores_normalizados


# Función de la integral
def f(x):
    return math.sin(math.pi * x)


# Calcular estimación, error estándar e intervalo de confianza
def calcular_resultados(valores_u, a, b, valor_teorico):
    valores_f = []

    for u in valores_u:
        # Transformar U(0,1) al intervalo [a,b]
        x = a + (b - a) * u
        valores_f.append(f(x))

    promedio = sum(valores_f) / len(valores_f)

    estimacion = (b - a) * promedio

    s_f = statistics.stdev(valores_f)

    error_estandar = (
        (b - a)
        * s_f
        / math.sqrt(len(valores_f))
    )

    limite_inferior = (
        estimacion - 1.96 * error_estandar
    )

    limite_superior = (
        estimacion + 1.96 * error_estandar
    )

    error_absoluto = abs(
        estimacion - valor_teorico
    )

    return (
        estimacion,
        error_estandar,
        limite_inferior,
        limite_superior,
        error_absoluto
    )


# Parámetros del experimento
a = 0
b = 1
n = 10000
semilla = 8103

valor_teorico = 2 / math.pi


# Generador estándar random
random.seed(semilla)

valores_random = []

for i in range(n):
    valores_random.append(random.random())

resultados_random = calcular_resultados(
    valores_random,
    a,
    b,
    valor_teorico
)


# Implementación propia de MT19937
_, valores_mt = mt19937(
    n,
    semilla
)

resultados_mt = calcular_resultados(
    valores_mt,
    a,
    b,
    valor_teorico
)


# Mostrar resultados
print("Comparación de generadores - Integral (a)")
print(f"N = {n}")
print(f"Semilla = {semilla}")
print(f"Valor teórico = {valor_teorico:.8f}")

print("\nrandom de Python")
print(
    f"Estimación Monte Carlo = "
    f"{resultados_random[0]:.8f}"
)
print(
    f"Error estándar = "
    f"{resultados_random[1]:.8f}"
)
print(
    f"IC 95% = "
    f"[{resultados_random[2]:.8f}, "
    f"{resultados_random[3]:.8f}]"
)
print(
    f"Error absoluto = "
    f"{resultados_random[4]:.8f}"
)

print("\nMT19937 propio")
print(
    f"Estimación Monte Carlo = "
    f"{resultados_mt[0]:.8f}"
)
print(
    f"Error estándar = "
    f"{resultados_mt[1]:.8f}"
)
print(
    f"IC 95% = "
    f"[{resultados_mt[2]:.8f}, "
    f"{resultados_mt[3]:.8f}]"
)
print(
    f"Error absoluto = "
    f"{resultados_mt[4]:.8f}"
)