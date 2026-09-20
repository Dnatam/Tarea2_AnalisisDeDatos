import random
import math


# Estimador de Monte Carlo para el volumen de la bola unitaria en d dimensiones
def volumen_bola_monte_carlo(d, n, semilla):
    random.seed(semilla)

    puntos_dentro = 0

    for i in range(n):
        suma_cuadrados = 0

        # Generar un punto en [-1,1]^d
        for j in range(d):
            x = random.uniform(-1, 1)
            suma_cuadrados += x**2

        # Verificar si el punto está dentro de la bola
        if suma_cuadrados <= 1:
            puntos_dentro += 1

    # Proporción de puntos dentro de la bola
    proporcion = puntos_dentro / n

    # Volumen del cubo [-1,1]^d
    volumen_cubo = 2**d

    # Estimación del volumen de la bola
    estimacion = volumen_cubo * proporcion

    # Error estándar estimado
    error_estandar = volumen_cubo * math.sqrt(
        proporcion * (1 - proporcion) / n
    )

    # Intervalo de confianza del 95 %
    limite_inferior = estimacion - 1.96 * error_estandar
    limite_superior = estimacion + 1.96 * error_estandar

    return (
        estimacion,
        error_estandar,
        limite_inferior,
        limite_superior,
        puntos_dentro,
        proporcion
    )


# Valor teórico del volumen de la bola se utiliza únicamente como referencia
def volumen_teorico(d):
    return (
        math.pi**(d / 2)
        / math.gamma(d / 2 + 1)
    )


# Parámetros
dimensiones = [2, 5, 10, 20]
n = 1000000
semilla = 8103


print("Volumen de la bola unitaria mediante Monte Carlo")
print(f"N = {n}")
print(f"Semilla = {semilla}")


for d in dimensiones:

    resultados = volumen_bola_monte_carlo(
        d,
        n,
        semilla
    )

    estimacion = resultados[0]
    error_estandar = resultados[1]
    limite_inferior = resultados[2]
    limite_superior = resultados[3]
    puntos_dentro = resultados[4]
    proporcion = resultados[5]

    teorico = volumen_teorico(d)

    error_absoluto = abs(
        estimacion - teorico
    )

    print(f"\nd = {d}")
    print(f"Puntos dentro = {puntos_dentro}")
    print(f"Proporción dentro = {proporcion:.10f}")
    print(f"Estimación Monte Carlo = {estimacion:.10f}")
    print(f"Error estándar = {error_estandar:.10f}")
    print(
        f"IC 95% = "
        f"[{limite_inferior:.10f}, "
        f"{limite_superior:.10f}]"
    )
    print(f"Valor teórico = {teorico:.10f}")
    print(f"Error absoluto = {error_absoluto:.10f}")