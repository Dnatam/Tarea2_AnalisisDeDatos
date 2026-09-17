import matplotlib.pyplot as plt
from scipy.stats import kstest, pearsonr

# Implementación del pseudocódigo
def mt19937(n, semilla):
    valores_enteros = []
    valores_normalizados = []

    # Vector de estado interno de 624 palabras
    estado = [0]*624

    estado[0] = semilla

    for i in range(1, 624):
        estado[i] = (1812433253 * (estado[i - 1] ^ (estado[i - 1] >> 30)) + i) % (2**32)

    # Generar n valores
    for k in range (n):
        y = ((estado[k % 624] & 0x80000000) | (estado[(k + 1) % 624] & 0x7FFFFFFF))

        # Aplicar la transformación twist
        if (y & 1) == 0:
            x = y >> 1
        else:
            x = (y >> 1) ^ 0x9908B0DF

        estado[k % 624] = (estado[(k + 397) % 624] ^ x)

        y = estado[k % 624]

        # Tempering
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9D2C5680)
        y = y ^ ((y << 15) & 0xEFC60000)
        y = y ^ (y >> 18)

        # Mantener el resultado en 32 bits
        y = y & 0xFFFFFFFF

        # Normalización
        r = y / (2**32)

        # Guardar los resultados
        valores_enteros.append(y)
        valores_normalizados.append(r)
    return valores_enteros, valores_normalizados

# Semilla inicial
semilla = 8103

# Cantidad de valores a generar
n= 10000

# Generar la secuencia
enteros, valores = mt19937(n, semilla)

# Mostrar los primeros valores
print("Mersenne Twister MT19937\n")
print("10 primeros valores generados")

for i in range(10):
    print(
        f"y{i + 1} = {enteros[i]} | "
        f"r{i + 1} = {valores[i]:.6f}"
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
plt.title("Histograma de valores generados por MT19937")
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
ax.set_title("Prueba espectral visual del MT19937")
ax.set_xlabel("u(i)")
ax.set_ylabel("u(i+1)")
ax.set_zlabel("u(i+2)")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
plt.savefig("prueba_espectral_mt19937.png", dpi=300, bbox_inches="tight")
plt.show()