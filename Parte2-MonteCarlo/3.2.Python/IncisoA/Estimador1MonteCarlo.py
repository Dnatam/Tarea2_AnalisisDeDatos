import random
import math
import statistics
import numpy as np
import matplotlib.pyplot as plt

# Función de la integral
def f(x):
    return math.sin(math.pi * x)

# Estimador de Monte Carlo
def monte_carlo_integral(a, b, n, semilla):
    random.seed(semilla)

    valores = []

    for i in range(n):
        u = random.uniform(a, b)
        valores.append(f(u))

    promedio = sum(valores) / n
    estimacion = (b - a) * promedio

    return estimacion, valores

a = 0
b = 1
n = 10000
semilla = 8103

# Generar la estimación de Monte Carlo
estimacion, valores = monte_carlo_integral(a, b, n, semilla)

# Valor teórico de la integral
valor_teorico = 2 / math.pi

# Desviación estándar muestral de f(U)
s_f = statistics.stdev(valores)

# Error estándar estimado
error_estandar = (b - a) * s_f / math.sqrt(n)

# Intervalo de confianza del 95 %
limite_inferior = estimacion - 1.96 * error_estandar
limite_superior = estimacion + 1.96 * error_estandar

# Error absoluto respecto al valor teórico
error_absoluto = abs(estimacion - valor_teorico)

# Mostrar resultados
print("Integral (a)")
print(f"N = {n}")
print(f"Semilla = {semilla}")
print(f"Estimación Monte Carlo = {estimacion:.8f}")
print(f"Error estándar = {error_estandar:.8f}")
print(
    f"IC 95% = "
    f"[{limite_inferior:.8f}, {limite_superior:.8f}]"
)
print(f"Valor teórico = {valor_teorico:.8f}")
print(f"Error absoluto = {error_absoluto:.8f}")

# Tamaños de muestra entre 10^1 y 10^6
tamanios_n = np.logspace(
    1,
    6,
    30,
    dtype=int
)

errores = []

print("\nEstudio de convergencia")

for n_actual in tamanios_n:
    estimacion_actual, _ = monte_carlo_integral(
        a,
        b,
        n_actual,
        semilla
    )

    error_actual = abs(
        estimacion_actual - valor_teorico
    )

    errores.append(error_actual)

    print(
        f"N = {n_actual:7d} | "
        f"Error absoluto = {error_actual:.8f}"
    )

# Ajustar una recta en escala log-log
log_n = np.log10(tamanios_n)
log_errores = np.log10(errores)

pendiente, intercepto = np.polyfit(
    log_n,
    log_errores,
    1
)

# Valores de la recta ajustada
recta_ajustada = (
    pendiente * log_n + intercepto
)

errores_ajustados = 10**recta_ajustada

print(
    f"\nPendiente estimada = "
    f"{pendiente:.4f}"
)

# Gráfica del estudio de convergencia
plt.figure()

plt.loglog(
    tamanios_n,
    errores,
    "o",
    label="Error absoluto"
)

plt.loglog(
    tamanios_n,
    errores_ajustados,
    label=f"Ajuste lineal (pendiente = {pendiente:.4f})"
)

plt.xlabel("N")
plt.ylabel("Error absoluto")
plt.title("Convergencia de Monte Carlo - Integral (a)")
plt.legend()
plt.grid(True, which="both")

plt.savefig(
    "convergencia_integral_a.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()