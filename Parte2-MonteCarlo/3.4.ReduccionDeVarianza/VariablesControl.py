import random
import math
import statistics

N = 10000
SEMILLA = 8103

A = 0.0
B = 2.0

VALOR_TEORICO = 0.4772498680518208


def normal_estandar(x):
    return (1 / math.sqrt(2 * math.pi)) * math.exp(-(x ** 2) / 2)


def monte_carlo_simple(n, semilla):
    random.seed(semilla)

    valores = []

    for _ in range(n):
        u = random.uniform(A, B)
        valores.append(normal_estandar(u))

    promedio = statistics.mean(valores)
    varianza_muestral = statistics.variance(valores)

    estimacion = (B - A) * promedio

    # Varianza y error estándar del estimador de la integral
    varianza_estimador = ((B - A) ** 2) * varianza_muestral / n
    error_estandar = math.sqrt(varianza_estimador)

    limite_inferior = estimacion - 1.96 * error_estandar
    limite_superior = estimacion + 1.96 * error_estandar

    error_absoluto = abs(estimacion - VALOR_TEORICO)

    return (
        estimacion,
        varianza_estimador,
        error_estandar,
        limite_inferior,
        limite_superior,
        error_absoluto
    )


def variables_control(n, semilla):
    random.seed(semilla)

    muestras_u = []
    valores_f = []

    for _ in range(n):
        u = random.uniform(A, B)
        muestras_u.append(u)
        valores_f.append(normal_estandar(u))

    promedio_u = statistics.mean(muestras_u)
    promedio_f = statistics.mean(valores_f)

    # Se estima Cov(f(U), U) y Var(U) con la muestra
    covarianza = sum(
        (valores_f[i] - promedio_f) * (muestras_u[i] - promedio_u)
        for i in range(n)
    ) / (n - 1)

    varianza_u = statistics.variance(muestras_u)

    c_estimado = covarianza / varianza_u

    # E[U] = 1 para U ~ Uniforme(0, 2)
    media_control = 1.0

    valores_corregidos = []

    for i in range(n):
        valor_corregido = (
            valores_f[i]
            - c_estimado * (muestras_u[i] - media_control)
        )
        valores_corregidos.append(valor_corregido)

    promedio_corregido = statistics.mean(valores_corregidos)
    varianza_corregida = statistics.variance(valores_corregidos)

    estimacion = (B - A) * promedio_corregido

    # Varianza y error estándar del estimador con variable de control
    varianza_estimador = ((B - A) ** 2) * varianza_corregida / n
    error_estandar = math.sqrt(varianza_estimador)

    limite_inferior = estimacion - 1.96 * error_estandar
    limite_superior = estimacion + 1.96 * error_estandar

    error_absoluto = abs(estimacion - VALOR_TEORICO)

    return (
        estimacion,
        varianza_estimador,
        error_estandar,
        limite_inferior,
        limite_superior,
        error_absoluto,
        c_estimado,
        covarianza
    )


resultado_mc = monte_carlo_simple(N, SEMILLA)
resultado_cv = variables_control(N, SEMILLA)

factor_reduccion = resultado_mc[1] / resultado_cv[1]

reduccion_porcentual = (
    1 - resultado_cv[1] / resultado_mc[1]
) * 100

speedup = factor_reduccion

print("Reducción de varianza - Variables de control")
print(f"N total de evaluaciones = {N}")
print(f"Semilla = {SEMILLA}")
print(f"Valor teórico = {VALOR_TEORICO:.8f}")

print("\nMonte Carlo simple")
print(f"Estimación = {resultado_mc[0]:.8f}")
print(f"Varianza del estimador = {resultado_mc[1]:.10f}")
print(f"Error estándar = {resultado_mc[2]:.8f}")
print(
    f"IC 95% = "
    f"[{resultado_mc[3]:.8f}, {resultado_mc[4]:.8f}]"
)
print(f"Error absoluto = {resultado_mc[5]:.8f}")

print("\nVariables de control")
print(f"Coeficiente c estimado = {resultado_cv[6]:.8f}")
print(f"Covarianza estimada = {resultado_cv[7]:.8f}")
print(f"Estimación = {resultado_cv[0]:.8f}")
print(f"Varianza del estimador = {resultado_cv[1]:.10f}")
print(f"Error estándar = {resultado_cv[2]:.8f}")
print(
    f"IC 95% = "
    f"[{resultado_cv[3]:.8f}, {resultado_cv[4]:.8f}]"
)
print(f"Error absoluto = {resultado_cv[5]:.8f}")

print("\nComparación")
print(f"Factor de reducción de varianza = {factor_reduccion:.4f}")
print(f"Reducción porcentual de varianza = {reduccion_porcentual:.2f}%")
print(f"Speedup equivalente = {speedup:.4f}x")