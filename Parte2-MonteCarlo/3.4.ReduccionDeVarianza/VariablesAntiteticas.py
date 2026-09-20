import random
import math
import statistics

# Función de la integral
def f(x):
    return (1 / math.sqrt(2 * math.pi)) * math.exp(-(x**2) / 2)

# Parámetros
a = 0
b = 2
n = 10000
semilla = 8103

# Valor teórico de la integral
valor_teorico = 0.47724987

# Monte Carlo simple
random.seed(semilla)

valores_mc = []

for i in range(n):
    u = random.uniform(a, b)
    valores_mc.append(f(u))

promedio_mc = sum(valores_mc) / n
estimacion_mc = (b - a) * promedio_mc

# Varianza y error estándar de Monte Carlo simple
varianza_mc = statistics.variance(valores_mc)

error_estandar_mc = (
    (b - a) * math.sqrt(varianza_mc) / math.sqrt(n)
)

varianza_estimador_mc = error_estandar_mc**2

# Intervalo de confianza del 95 %
limite_inferior_mc = estimacion_mc - 1.96 * error_estandar_mc
limite_superior_mc = estimacion_mc + 1.96 * error_estandar_mc

error_absoluto_mc = abs(estimacion_mc - valor_teorico)

# Variables antitéticas
# Cada par utiliza dos evaluaciones de la función
numero_pares = n // 2

random.seed(semilla)

valores_antiteticos = []

for i in range(numero_pares):
    u = random.uniform(a, b)

    # Variable antitética en el intervalo [0, 2]
    u_antitetica = a + b - u

    # Promedio de las dos evaluaciones del par
    promedio_par = (f(u) + f(u_antitetica)) / 2
    valores_antiteticos.append(promedio_par)

promedio_antitetico = (
    sum(valores_antiteticos) / numero_pares
)

estimacion_antitetica = (
    (b - a) * promedio_antitetico
)

# Varianza y error estándar del estimador antitético
varianza_antitetica = statistics.variance(
    valores_antiteticos
)

error_estandar_antitetico = (
    (b - a)
    * math.sqrt(varianza_antitetica)
    / math.sqrt(numero_pares)
)

varianza_estimador_antitetico = (
    error_estandar_antitetico**2
)

# Intervalo de confianza del 95 %
limite_inferior_antitetico = (
    estimacion_antitetica
    - 1.96 * error_estandar_antitetico
)

limite_superior_antitetico = (
    estimacion_antitetica
    + 1.96 * error_estandar_antitetico
)

error_absoluto_antitetico = abs(
    estimacion_antitetica - valor_teorico
)

# Factor de reducción de varianza
factor_reduccion = (
    varianza_estimador_mc
    / varianza_estimador_antitetico
)

reduccion_porcentual = (
    1
    - varianza_estimador_antitetico
    / varianza_estimador_mc
) * 100

# Speedup equivalente respecto a Monte Carlo simple
speedup = factor_reduccion

# Mostrar resultados
print("Reducción de varianza - Variables antitéticas")
print(f"N total de evaluaciones = {n}")
print(f"Semilla = {semilla}")
print(f"Valor teórico = {valor_teorico:.8f}")

print("\nMonte Carlo simple")
print(f"Estimación = {estimacion_mc:.8f}")
print(f"Varianza del estimador = {varianza_estimador_mc:.10f}")
print(f"Error estándar = {error_estandar_mc:.8f}")
print(
    f"IC 95% = "
    f"[{limite_inferior_mc:.8f}, {limite_superior_mc:.8f}]"
)
print(f"Error absoluto = {error_absoluto_mc:.8f}")

print("\nVariables antitéticas")
print(f"Número de pares = {numero_pares}")
print(f"Evaluaciones totales = {2 * numero_pares}")
print(f"Estimación = {estimacion_antitetica:.8f}")
print(
    f"Varianza del estimador = "
    f"{varianza_estimador_antitetico:.10f}"
)
print(f"Error estándar = {error_estandar_antitetico:.8f}")
print(
    f"IC 95% = "
    f"[{limite_inferior_antitetico:.8f}, "
    f"{limite_superior_antitetico:.8f}]"
)
print(f"Error absoluto = {error_absoluto_antitetico:.8f}")

print("\nComparación")
print(f"Factor de reducción de varianza = {factor_reduccion:.4f}")
print(f"Reducción porcentual de varianza = {reduccion_porcentual:.2f}%")
print(f"Speedup equivalente = {speedup:.4f}x")