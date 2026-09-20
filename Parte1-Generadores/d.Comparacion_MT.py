import random
import secrets
import time
import matplotlib.pyplot as plt
from scipy.stats import kstest, pearsonr

# Implementación propia de Mersenne Twister MT19937
def mt19937(n, semilla):
    valores_enteros = []
    valores_normalizados = []

    # Vector de estado interno de 624 palabras
    estado = [0] * 624
    estado[0] = semilla

    # Inicializar el estado interno a partir de la semilla
    for i in range(1, 624):
        estado[i] = (
            1812433253 * (estado[i - 1] ^ (estado[i - 1] >> 30)) + i
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

        estado[k % 624] = estado[(k + 397) % 624] ^ x
        y = estado[k % 624]

        # Aplicar tempering
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9D2C5680)
        y = y ^ ((y << 15) & 0xEFC60000)
        y = y ^ (y >> 18)

        # Mantener el resultado en 32 bits
        y = y & 0xFFFFFFFF

        # Normalizar el valor al intervalo [0,1)
        r = y / (2**32)

        valores_enteros.append(y)
        valores_normalizados.append(r)

    return valores_enteros, valores_normalizados

# Semilla utilizada para MT19937 y random
semilla = 8103

# Cantidad de valores a generar con cada método
n = 10000

# Medir el tiempo de generación de MT19937 propio
inicio = time.perf_counter()
_, valores_mt = mt19937(n, semilla)
fin = time.perf_counter()

tiempo_mt = fin - inicio

# Utilizar la misma semilla para reproducibilidad con random
random.seed(semilla)

# Medir el tiempo de generación con random
inicio = time.perf_counter()

valores_random = [
    random.random()
    for _ in range(n)
]

fin = time.perf_counter()

tiempo_random = fin - inicio

# Medir el tiempo de generación con secrets, este utiliza la fuente de aleatoriedad del sistema operativo
inicio = time.perf_counter()

valores_secrets = [
    secrets.randbits(32) / (2**32)
    for _ in range(n)
]

fin = time.perf_counter()

tiempo_secrets = fin - inicio

# Aplicar las mismas pruebas estadísticas a cada generador
def analizar(nombre, valores, tiempo):

    # Prueba de uniformidad Kolmogorov-Smirnov
    estadistico_ks, p_ks = kstest(
        valores,
        "uniform"
    )

    # Prueba de independencia serial mediante correlación de retardo 1
    correlacion, p_corr = pearsonr(
        valores[:-1],
        valores[1:]
    )
    print(f"\n{nombre}")
    print(f"Tiempo de generación: {tiempo:.8f} segundos")
    print("\nPrueba de uniformidad Kolmogorov-Smirnov")
    print(f"Estadístico K-S: {estadistico_ks:.6f}")
    print(f"p-valor: {p_ks:.6e}")
    print("\nPrueba de independencia serial - Autocorrelación de retardo 1")
    print(f"Estadístico de correlación: {correlacion:.6f}")
    print(f"p-valor: {p_corr:.6e}")

    return estadistico_ks, p_ks, correlacion, p_corr

# Analizar los valores obtenidos con los tres métodos
print("Comparación de MT19937, random y secrets")
print(f"\nCantidad de valores: {n}")
print(f"Semilla para MT19937 y random: {semilla}")

resultado_mt = analizar("MT19937 propio", valores_mt, tiempo_mt)

resultado_random = analizar("random", valores_random, tiempo_random)

resultado_secrets = analizar("secrets", valores_secrets, tiempo_secrets)

# Crear histogramas para comparar visualmente las distribuciones
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].hist(valores_mt, bins=20, edgecolor="black")
axes[0].set_title("MT19937 propio")
axes[0].set_xlabel("Valor normalizado")
axes[0].set_ylabel("Frecuencia")
axes[0].set_xlim(0, 1)
axes[1].hist(valores_random, bins=20, edgecolor="black")
axes[1].set_title("random")
axes[1].set_xlabel("Valor normalizado")
axes[1].set_ylabel("Frecuencia")
axes[1].set_xlim(0, 1)

axes[2].hist(valores_secrets, bins=20, edgecolor="black")
axes[2].set_title("secrets")
axes[2].set_xlabel("Valor normalizado")
axes[2].set_ylabel("Frecuencia")
axes[2].set_xlim(0, 1)
plt.suptitle("Comparación de distribuciones")
plt.tight_layout()

# Guardar la figura para incluirla en el documento
plt.savefig(
    "comparacion_mt_random_secrets.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()