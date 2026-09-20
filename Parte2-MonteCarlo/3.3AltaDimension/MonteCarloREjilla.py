import random
import math
import itertools


# Estimación mediante Monte Carlo
def volumen_monte_carlo(d, n, semilla):
    random.seed(semilla)

    puntos_dentro = 0

    for i in range(n):
        suma_cuadrados = 0

        for j in range(d):
            x = random.uniform(-1, 1)
            suma_cuadrados += x**2

        if suma_cuadrados <= 1:
            puntos_dentro += 1

    proporcion = puntos_dentro / n
    estimacion = (2**d) * proporcion

    return estimacion


# Estimación mediante rejilla determinística
def volumen_rejilla(d, m):
    # Centros de las m divisiones de [-1,1]
    ancho = 2 / m

    centros = [
        -1 + (i + 0.5) * ancho
        for i in range(m)
    ]

    puntos_dentro = 0
    puntos_totales = m**d

    # Producto cartesiano de los centros
    for punto in itertools.product(
        centros,
        repeat=d
    ):
        suma_cuadrados = sum(
            x**2 for x in punto
        )

        if suma_cuadrados <= 1:
            puntos_dentro += 1

    proporcion = puntos_dentro / puntos_totales
    estimacion = (2**d) * proporcion

    return estimacion, puntos_totales


# Valor exacto utilizado únicamente como referencia
def volumen_teorico(d):
    return (
        math.pi**(d / 2)
        / math.gamma(d / 2 + 1)
    )


# Buscar el mayor m cuyo número de puntos
# no supere el presupuesto
def obtener_m(d, presupuesto):
    m = int(
        presupuesto**(1 / d)
    )

    while (m + 1)**d <= presupuesto:
        m += 1

    while m**d > presupuesto:
        m -= 1

    return m


dimensiones = [2, 5, 10, 20]
presupuesto = 1000000
semilla = 8103


print("Comparación Monte Carlo vs rejilla determinística")
print(f"Presupuesto máximo = {presupuesto}")


for d in dimensiones:
    m = obtener_m(
        d,
        presupuesto
    )

    puntos_rejilla = m**d

    # Usar en Monte Carlo el mismo número
    # de puntos que utiliza la rejilla
    estimacion_mc = volumen_monte_carlo(
        d,
        puntos_rejilla,
        semilla
    )

    estimacion_rejilla, _ = volumen_rejilla(
        d,
        m
    )

    teorico = volumen_teorico(d)

    error_mc = abs(
        estimacion_mc - teorico
    )

    error_rejilla = abs(
        estimacion_rejilla - teorico
    )

    print(f"\nd = {d}")
    print(f"m = {m}")
    print(f"Puntos utilizados = {puntos_rejilla}")
    print(f"Valor teórico = {teorico:.10f}")
    print(
        f"Monte Carlo = {estimacion_mc:.10f} | "
        f"Error = {error_mc:.10f}"
    )
    print(
        f"Rejilla = {estimacion_rejilla:.10f} | "
        f"Error = {error_rejilla:.10f}"
    )


# Crecimiento de una rejilla con m = 10
print("\nCrecimiento de la rejilla con m = 10")

for d in dimensiones:
    puntos = 10**d

    print(
        f"d = {d:2d} | "
        f"Puntos = {puntos}"
    )