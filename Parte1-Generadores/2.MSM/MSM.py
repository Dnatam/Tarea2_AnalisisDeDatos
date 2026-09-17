import matplotlib.pyplot as plt
from scipy.stats import kstest, pearsonr

# Implementación del pseudocódigo
def msm(semilla, d, n):
    valores_enteros = []
    valores_normalizados = []

    # X0
    X = semilla
    for i in range(n):
        cuadrado = X**2

        truncado = cuadrado // (10**(d // 2))

        X = truncado % (10**d)

        r = X / (10**d)

        valores_enteros.append(X)
        valores_normalizados.append(r)
    return valores_enteros, valores_normalizados

# Semilla inicial
semilla = 8103

# Cantidad de dígitos
d = 4

# Cantidad de valores a generar
n = 10000

# Generar la secuencia
enteros, valores = msm(semilla, d, n)

# Mostrar los primeros valores 
print("Métodos de Cuadrados Medios (MSM)\n")
print("20 primeros valores generados")
for i in range(20):
    print(
        f"X{i + 1} = {enteros[i]:0{d}d} | "
        f"u{i + 1} = {valores[i]:.6f}"
    )

# Prueba de uniformidad
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
plt.hist(valores, bins=20, edgecolor="black")
plt.title("Histograma de valores generados por MSM")
plt.xlabel("Valor normalizado")
plt.ylabel("Frecuencia")
plt.xlim(0, 1)
plt.savefig("histograma_msm.png", dpi=300, bbox_inches="tight")
plt.show()


# Prueba espectral visual
x = valores[:-2]
y = valores[1:-1]
z = valores[2:]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(x, y, z, s=2)
ax.set_title("Prueba espectral visual del MSM")
ax.set_xlabel("u(i)")
ax.set_ylabel("u(i+1)")
ax.set_zlabel("u(i+2)")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
plt.savefig("prueba_espectral_msm.png", dpi=300, bbox_inches="tight")
plt.show()