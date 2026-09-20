import math
import matplotlib.pyplot as plt

# Volumen exacto de la bola unitaria
def volumen_bola(d):
    return (
        math.pi**(d / 2)
        / math.gamma(d / 2 + 1)
    )

# Dimensiones que se analizarán
dimensiones = list(range(1, 21))

fracciones = []

for d in dimensiones:
    volumen = volumen_bola(d)

    # Volumen del hipercubo [-1,1]^d
    volumen_cubo = 2**d

    # Fracción del hipercubo ocupada por la bola
    fraccion = volumen / volumen_cubo

    fracciones.append(fraccion)

    print(
        f"d = {d:2d} | "
        f"V_d / 2^d = {fraccion:.10e}"
    )

# Graficar la fracción de volumen
plt.figure()

plt.plot(
    dimensiones,
    fracciones,
    marker="o"
)

plt.xlabel("Dimensión d")
plt.ylabel("Fracción de volumen V_d / 2^d")
plt.title("Fracción del hipercubo ocupada por la bola unitaria")
plt.grid(True)

plt.savefig(
    "fraccion_volumen.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()