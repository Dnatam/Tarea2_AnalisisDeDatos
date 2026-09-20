import matplotlib.pyplot as plt
from scipy.stats import kstest, pearsonr

# Implementación del pseudocódigo
# Verificar si un número es primo
def es_primo(numero):
    if numero < 2:
        return False

    divisor = 2

    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False

        divisor += 1

    return True

# Calcular el máximo común divisor
def calcular_mcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a

# Generador Blum Blum Shub
def bbs(p, q, semilla, n, k):
    valores_enteros = []
    valores_normalizados = []

    # Validar p
    if not es_primo(p) or p % 4 != 3:
        raise ValueError(
            "p debe ser primo y congruente con 3 módulo 4"
        )

    # Validar q
    if not es_primo(q) or q % 4 != 3 or q == p:
        raise ValueError(
            "q debe ser primo, distinto de p "
            "y congruente con 3 módulo 4"
        )

    M = p * q

    # Validar la semilla
    if (
        semilla == 0
        or semilla == 1
        or calcular_mcd(semilla, M) != 1
    ):
        raise ValueError(
            "La semilla debe ser distinta de 0 y 1 "
            "y coprima con M"
        )

    # Estado inicial
    X = (semilla**2) % M

    # Generar n números
    for i in range(n):
        R = 0

        # Construir R utilizando k bits
        for j in range(k):
            # Recurrencia BBS
            X = (X**2) % M

            # Extraer el bit menos significativo
            bit = X % 2

            # Agregar el bit al número R
            R = (R * 2) + bit

        # Normalización
        u = R / (2**k)

        # Guardar resultados
        valores_enteros.append(R)
        valores_normalizados.append(u)

    return valores_enteros, valores_normalizados

# Parámetros de BBS
p = 383
q = 503

# Semilla inicial
semilla = 8103

# Cantidad de valores a generar
n = 10000

# Cantidad de bits utilizados para formar cada número
k = 16


# Generar la secuencia
enteros, valores = bbs(p, q, semilla, n, k)

# Mostrar los primeros valores
print("Blum Blum Shub (BBS)\n")
print(f"p = {p}")
print(f"q = {q}")
print(f"M = {p * q}")
print(f"semilla = {semilla}")
print(f"k = {k}\n")
print("10 primeros valores generados")
for i in range(10):
    print(
        f"R{i + 1} = {enteros[i]} | "
        f"u{i + 1} = {valores[i]:.6f}"
    )

# Prueba de uniformidad
estadistico_ks, p_valor = kstest(valores, "uniform")
print("\nPrueba de uniformidad Kolmogorov-Smirnov")
print(f"Estadístico K-S: {estadistico_ks:.6f}")
print(f"p-valor: {p_valor:.6e}")

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
print(f"p-valor: {p_valor_corr:.6e}")

# Interpretación de la prueba
if p_valor_corr > alpha:
    print("No se rechaza H0, no existe evidencia de correlación lineal significativa entre valores consecutivos.")
else:
    print("Se rechaza H0, existe evidencia de correlación lineal significativa entre valores consecutivos.")

# Histograma de los valores normalizados
plt.hist(valores, bins=20, edgecolor="black")
plt.title("Histograma de valores generados por BBS")
plt.xlabel("Valor normalizado")
plt.ylabel("Frecuencia")
plt.xlim(0, 1)
plt.savefig("histograma_bbs.png", dpi=300, bbox_inches="tight")
plt.show()

# Prueba espectral visual
x = valores[:-2]
y = valores[1:-1]
z = valores[2:]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(x, y, z, s=2)
ax.set_title("Prueba espectral visual de BBS")
ax.set_xlabel("u(i)")
ax.set_ylabel("u(i+1)")
ax.set_zlabel("u(i+2)")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
plt.savefig("prueba_espectral_bbs.png", dpi=300, bbox_inches="tight")
plt.show()

# Cantidad de ternas distintas
ternas = list(zip(
    valores[:-2],
    valores[1:-1],
    valores[2:]
))

ternas_distintas = len(set(ternas))

print("\nAnálisis de ternas")
print(f"Ternas totales: {len(ternas)}")
print(f"Ternas distintas: {ternas_distintas}")
print(f"Ternas repetidas: {len(ternas) - ternas_distintas}")