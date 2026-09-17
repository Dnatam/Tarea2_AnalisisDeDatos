import matplotlib.pyplot as plt
import math
from scipy.stats import kstest, pearsonr


# Implementación del pseudocódigo
def lcg(semilla, m, a, c, n):
    valores_enteros = []
    valores_normalizados = []

    # X0
    X = semilla

    for i in range(n):
        X = (a * X + c) % m # Fórmula del LCG
        u = X / m # Normalización

        # Guarda los resultados en el arreglo
        valores_enteros.append(X)
        valores_normalizados.append(u)

    return valores_enteros, valores_normalizados

# Semilla inicial
semilla = 8102003

# Cantidad de valores a generar
n = 10000

# Utilicé parámetros conocidos del generador Numerical Recipes
m = 2**32
a = 1664525
c = 1013904223

# Verificación de las condiciones de Hull-Dobell

print("\nVerificación de Hull-Dobell")

print(
    "1. MCD(c, m) = 1:",
    math.gcd(c, m) == 1
)

print(
    "2. (a - 1) es divisible por 2:",
    (a - 1) % 2 == 0
)

print(
    "3. (a - 1) es divisible por 4:",
    (a - 1) % 4 == 0
)

# Generar la secuencia
enteros, valores = lcg(semilla, m, a, c, n)

print("Generador Congruencial Lineal (LCG)\n")
print("10 primeros valores generados")
for i in range(10):
    print(
        f"X{i + 1} = {enteros[i]} | "
        f"u{i + 1} = {valores[i]:.6f}"
    )

#Prueba de uniformidad
estadistico_ks, p_valor = kstest(valores, "uniform") 

print("\nPrueba de uniformidad Kolmogorov-Smirnov")
print(f"Estadístico K-S: {estadistico_ks:.6f}")
print(f"p-valor: {p_valor:.6f}")

# Nivel de significancia
alpha = 0.05

# Interpretación de la prueba
if p_valor > alpha:
    print("No se rechaza H0, los resultados son compatibles con una distribución uniforme.")
else:
    print("Se rechaza H0, los resultados presentan evidencia contra una distribución uniforme.")

# Prueba de independencia
estadistico_corr, p_valor_corr = pearsonr(valores[:-1], valores[1:])

print("\nPrueba de independencia serial - Autocorrelación de retardo 1")
print(f"Estadístico de correlación: {estadistico_corr:.6f}")
print(f"p-valor: {p_valor_corr:.6f}")

# Interpretación de la prueba
if p_valor_corr > alpha:
    print("No se rechaza H0, no existe evidencia de correlación lineal significativa entre valores consecutivos.")
else:
    print("Se rechaza H0, existe evidencia de correlación lineal significativa entre valores consecutivos.")

# Histograma de los valores normalizados
plt.hist( valores, bins=20, edgecolor="black")
plt.title("Histograma de valores generados por LCG")
plt.xlabel("Valor normalizado")
plt.ylabel("Frecuencia")
plt.xlim(0, 1)
plt.savefig("histograma_lcg.png", dpi=300, bbox_inches="tight")
plt.show()

# Prueba espectral visual
x = valores[:-2]
y = valores[1:-1]
z = valores[2:]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(x, y, z, s=2)
ax.set_title("Prueba espectral visual del LCG")
ax.set_xlabel("u(i)")
ax.set_ylabel("u(i+1)")
ax.set_zlabel("u(i+2)")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
plt.savefig("prueba_espectral_lcg.png", dpi=300, bbox_inches="tight")
plt.show()