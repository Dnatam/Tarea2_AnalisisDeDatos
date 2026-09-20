import matplotlib.pyplot as plt
from scipy.stats import kstest, pearsonr

# Implementación del pseudocódigo
def randu(semilla, n):
    valores_enteros = []
    valores_normalizados = []

    # Validar que la semilla sea impar
    if semilla % 2 == 0:
        raise ValueError(
            "La semilla debe ser un número impar"
        )

    # Valor inicial
    V = semilla

    # Generar n valores
    for i in range(n):

        # Fórmula de RANDU
        V = (65539 * V) % (2**31)

        # Normalización
        U = V / (2**31)

        # Guardar resultados
        valores_enteros.append(V)
        valores_normalizados.append(U)

    return valores_enteros, valores_normalizados

# Semilla inicial
semilla = 8103

# Cantidad de valores a generar
n = 10000

# Generar la secuencia
enteros, valores = randu(
    semilla,
    n
)

# Mostrar los primeros valores
print("RANDU\n")
print(f"Semilla = {semilla}")
print(f"Cantidad de valores = {n}\n")
print("10 primeros valores generados")
for i in range(10):
    print(
        f"V{i + 1} = {enteros[i]} | "
        f"U{i + 1} = {valores[i]:.6f}"
    )


# PRUEBA DE UNIFORMIDAD
estadistico_ks, p_valor = kstest(
    valores,
    "uniform"
)

print("\nPrueba de uniformidad Kolmogorov-Smirnov")
print(f"Estadístico K-S: {estadistico_ks:.6f}")
print(f"p-valor: {p_valor:.6e}")

# Nivel de significancia
alpha = 0.05

# Interpretación de la prueba
if p_valor > alpha:
    print(
        "No se rechaza H0, los resultados son compatibles con una distribución uniforme."
    )
else:
    print(
        "Se rechaza H0, los resultados presentan evidencia contra una distribución uniforme."
    )


# PRUEBA DE INDEPENDENCIA SERIAL

estadistico_corr, p_valor_corr = pearsonr(
    valores[:-1],
    valores[1:]
)

print(
    "\nPrueba de independencia serial - Autocorrelación de retardo 1"
)

print(
    f"Estadístico de correlación: "
    f"{estadistico_corr:.6f}"
)

print(
    f"p-valor: {p_valor_corr:.6e}"
)

# Interpretación de la prueba
if p_valor_corr > alpha:
    print(
        "No se rechaza H0, no existe evidencia de correlación lineal significativa entre valores consecutivos."
    )
else:
    print(
        "Se rechaza H0, existe evidencia de correlación lineal significativa entre valores consecutivos."
    )

# HISTOGRAMA
plt.hist(
    valores,
    bins=20,
    edgecolor="black"
)

plt.title(
    "Histograma de valores generados por RANDU"
)

plt.xlabel("Valor normalizado")
plt.ylabel("Frecuencia")

plt.xlim(0, 1)

plt.savefig(
    "histograma_randu.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

x = valores[:-2]
y = valores[1:-1]
z = valores[2:]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(
    x,
    y,
    z,
    s=1,
    alpha=0.35
)

ax.set_title("Prueba espectral visual de RANDU")

ax.set_xlabel("u(i)")
ax.set_ylabel("u(i+1)")
ax.set_zlabel("u(i+2)")

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

# Ángulo que permite observar mejor los planos
ax.view_init(
    elev=17,
    azim=60,
    roll=-3
)

plt.savefig(
    "prueba_espectral_randu.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ANÁLISIS DE TERNAS

ternas = list(
    zip(
        valores[:-2],
        valores[1:-1],
        valores[2:]
    )
)

ternas_distintas = len(
    set(ternas)
)

print("\nAnálisis de ternas")

print(
    f"Ternas totales: "
    f"{len(ternas)}"
)

print(
    f"Ternas distintas: "
    f"{ternas_distintas}"
)

print(
    f"Ternas repetidas: "
    f"{len(ternas) - ternas_distintas}"
)


# VERIFICACIÓN DE LOS PLANOS DE RANDU
planos = []

for i in range(len(valores) - 2):

    k = round(
        valores[i + 2]
        - 6 * valores[i + 1]
        + 9 * valores[i]
    )

    planos.append(k)


planos_distintos = sorted(
    set(planos)
)

print(
    "\nAnálisis de planos de RANDU"
)

print(
    f"Valores de k: "
    f"{planos_distintos}"
)

print(
    f"Cantidad de planos: "
    f"{len(planos_distintos)}"
)