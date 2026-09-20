import math
import matplotlib.pyplot as plt

# Implementación de RANDU
def randu(semilla, n):
    valores = []

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

        # Guardar resultado
        valores.append(U)

    return valores


# Implementación de Mersenne Twister MT19937
def mt19937(n, semilla):
    valores = []

    # Vector de estado interno de 624 palabras
    estado = [0] * 624

    # Valor inicial
    estado[0] = semilla

    # Inicializar el vector de estado
    for i in range(1, 624):
        estado[i] = (
            1812433253
            * (
                estado[i - 1]
                ^ (estado[i - 1] >> 30)
            )
            + i
        ) % (2**32)

    # Generar n valores
    for k in range(n):

        y = (
            (estado[k % 624] & 0x80000000)
            | (
                estado[(k + 1) % 624]
                & 0x7FFFFFFF
            )
        )

        # Aplicar la transformación twist
        if (y & 1) == 0:
            x = y >> 1
        else:
            x = (
                (y >> 1)
                ^ 0x9908B0DF
            )

        estado[k % 624] = (
            estado[(k + 397) % 624]
            ^ x
        )

        y = estado[k % 624]

        # Tempering
        y = y ^ (y >> 11)
        y = y ^ (
            (y << 7)
            & 0x9D2C5680
        )
        y = y ^ (
            (y << 15)
            & 0xEFC60000
        )
        y = y ^ (y >> 18)

        # Mantener el resultado en 32 bits
        y = y & 0xFFFFFFFF

        # Normalización
        U = y / (2**32)

        # Guardar resultado
        valores.append(U)

    return valores


# Estimación del volumen de la bola unitaria
def estimar_volumen(valores, n_puntos):

    # Contador de puntos dentro de la bola
    puntos_dentro = 0

    # Formar puntos con ternas consecutivas
    for i in range(n_puntos):

        x = valores[3 * i]
        y = valores[3 * i + 1]
        z = valores[3 * i + 2]

        # Verificar si el punto está dentro de la bola
        if x**2 + y**2 + z**2 <= 1:
            puntos_dentro += 1

    # Proporción de puntos dentro
    proporcion = puntos_dentro / n_puntos

    # Estimar el volumen completo de la bola
    volumen = 8 * proporcion

    # Calcular el error estándar
    error_estandar_proporcion = math.sqrt(
        proporcion
        * (1 - proporcion)
        / n_puntos
    )

    error_estandar = (
        8 * error_estandar_proporcion
    )

    # Calcular intervalo de confianza del 95%
    limite_inferior = (
        volumen
        - 1.96 * error_estandar
    )

    limite_superior = (
        volumen
        + 1.96 * error_estandar
    )

    return (
        volumen,
        error_estandar,
        limite_inferior,
        limite_superior,
        puntos_dentro
    )


# Semilla inicial
semilla = 8103

# Cantidad de puntos tridimensionales
n_puntos = 100000

# Cada punto utiliza tres valores
n_valores = 3 * n_puntos

# Valor teórico del volumen de la bola unitaria
valor_teorico = 4 * math.pi / 3


# Generar valores con RANDU
valores_randu = randu(
    semilla,
    n_valores
)

# Estimar volumen con RANDU
(
    estimacion_randu,
    error_estandar_randu,
    limite_inferior_randu,
    limite_superior_randu,
    puntos_dentro_randu
) = estimar_volumen(
    valores_randu,
    n_puntos
)


# Generar valores con MT19937
valores_mt = mt19937(
    n_valores,
    semilla
)

# Estimar volumen con MT19937
(
    estimacion_mt,
    error_estandar_mt,
    limite_inferior_mt,
    limite_superior_mt,
    puntos_dentro_mt
) = estimar_volumen(
    valores_mt,
    n_puntos
)


# Calcular errores absolutos
error_randu = abs(
    estimacion_randu
    - valor_teorico
)

error_mt = abs(
    estimacion_mt
    - valor_teorico
)


# Mostrar información del experimento
print("Caso RANDU - Monte Carlo en 3D\n")

print(
    f"Número de puntos 3D = {n_puntos}"
)

print(
    f"Número de valores generados = {n_valores}"
)

print(
    f"Semilla = {semilla}"
)

print(
    f"Valor teórico = {valor_teorico:.8f}"
)


# Mostrar resultados de RANDU
print("\nRANDU")

print(
    f"Puntos dentro = {puntos_dentro_randu}"
)

print(
    f"Estimación = {estimacion_randu:.8f}"
)

print(
    f"Error estándar = "
    f"{error_estandar_randu:.8f}"
)

print(
    "IC 95% = "
    f"[{limite_inferior_randu:.8f}, "
    f"{limite_superior_randu:.8f}]"
)

print(
    f"Error absoluto = {error_randu:.8f}"
)


# Mostrar resultados de MT19937
print("\nMersenne Twister MT19937")

print(
    f"Puntos dentro = {puntos_dentro_mt}"
)

print(
    f"Estimación = {estimacion_mt:.8f}"
)

print(
    f"Error estándar = "
    f"{error_estandar_mt:.8f}"
)

print(
    "IC 95% = "
    f"[{limite_inferior_mt:.8f}, "
    f"{limite_superior_mt:.8f}]"
)

print(
    f"Error absoluto = {error_mt:.8f}"
)


# Comparar los errores
print("\nComparación")

if error_randu > error_mt:

    razon = error_randu / error_mt

    print(
        "RANDU presentó un error absoluto "
        f"{razon:.4f} veces mayor que MT19937."
    )

else:

    razon = error_mt / error_randu

    print(
        "MT19937 presentó un error absoluto "
        f"{razon:.4f} veces mayor que RANDU "
        "en esta ejecución."
    )

# Cantidad de puntos que se mostrarán
n_grafica = 5000

# Preparar puntos generados por RANDU
x_randu = []
y_randu = []
z_randu = []

for i in range(n_grafica):

    x_randu.append(
        valores_randu[3 * i]
    )

    y_randu.append(
        valores_randu[3 * i + 1]
    )

    z_randu.append(
        valores_randu[3 * i + 2]
    )

# Gráfica tridimensional de RANDU
fig = plt.figure(
    figsize=(10, 8)
)

ax = fig.add_subplot(
    111,
    projection="3d"
)

ax.scatter(
    x_randu,
    y_randu,
    z_randu,
    s=2,
    alpha=0.4
)

ax.set_title(
    "Puntos tridimensionales generados por RANDU"
)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

# Ajustar el ángulo para observar la estructura
ax.view_init(
    elev=17,
    azim=60,
    roll=-3
)

plt.savefig(
    "puntos_3d_randu.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Preparar puntos generados por MT19937
x_mt = []
y_mt = []
z_mt = []

for i in range(n_grafica):

    x_mt.append(
        valores_mt[3 * i]
    )

    y_mt.append(
        valores_mt[3 * i + 1]
    )

    z_mt.append(
        valores_mt[3 * i + 2]
    )

# Gráfica tridimensional de MT19937
fig = plt.figure(
    figsize=(10, 8)
)

ax = fig.add_subplot(
    111,
    projection="3d"
)

ax.scatter(
    x_mt,
    y_mt,
    z_mt,
    s=2,
    alpha=0.4
)

ax.set_title(
    "Puntos tridimensionales generados por MT19937"
)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

plt.savefig(
    "puntos_3d_mt19937.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()