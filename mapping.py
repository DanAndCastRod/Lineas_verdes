import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def crear_mapa_de_calor(n, m, k):
    # Generar matriz aleatoria de nxm con valores de 0 a k
    vegetacion = np.random.randint(k, size = (n,m))

    # paleta de colores
    verde = ['#C7EA46', '#9ED14A', '#6FBF4A', '#4DAF4A', '#2D9440', '#157F3E']
    cmap = ListedColormap(verde)

    # Crear mapa de calor
    fig, ax = plt.subplots()
    im = ax.imshow(vegetacion, cmap = cmap)
    

    ## Añadir leyenda
    cbar = ax.figure.colorbar(im, ax = ax)
    cbar.ax.set_ylabel("Nivel de vegetación", rotation = -90, va = 'bottom')

    plt.show()


def crear_mapa_de_calor_relieve():
    # Generar matriz aleatoria de 100x100 con valores entre 0 y 1
    relieve = np.random.rand(100, 100)

    # Convertir matriz aleatoria en relieve utilizando función sigmoidal
    relieve = 1 / (1 + np.exp(-10*(relieve-0.5)))

    # Crear paleta de colores para relieve
    marron = ['#E7CBA9', '#CEAA7B', '#B5874E', '#965927', '#603813']
    cmap = ListedColormap(marron)

    # Crear mapa de calor para relieve
    fig, ax = plt.subplots()
    im = ax.imshow(relieve, cmap=cmap)

    # Añadir leyenda
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Relieve", rotation=-90, va="bottom")

    # Mostrar mapa de calor
    plt.show()

def crear_mapa_de_calor_hidrico():
    # Generar matriz aleatoria de 100x100 con valores entre 0 y 1
    hidrico = np.random.rand(100, 100)

    # Convertir matriz aleatoria en recursos hídricos utilizando función sigmoidal
    hidrico = 1 / (1 + np.exp(-10*(hidrico-0.5)))

    # Crear paleta de colores para recursos hídricos
    azul = ['#D7EFFF', '#A4C8FF', '#6AAFFF', '#2674FF', '#0045B5']
    cmap = ListedColormap(azul)

    # Crear mapa de calor para recursos hídricos
    fig, ax = plt.subplots()
    im = ax.imshow(hidrico, cmap=cmap)

    # Añadir leyenda
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Recursos hídricos", rotation=-90, va="bottom")

    # Mostrar mapa de calor
    plt.show()

def crear_mapa_de_calor_boscoso():
    # Generar matriz aleatoria de 100x100 con valores entre 0 y 1
    boscoso = np.random.rand(100, 100)

    # Convertir matriz aleatoria en zonas boscosas utilizando función sigmoidal
    boscoso = 1 / (1 + np.exp(-10*(boscoso-0.5)))

    # Crear paleta de colores para zonas boscosas
    verde = ['#C7EA46', '#9ED14A', '#6FBF4A', '#4DAF4A', '#2D9440', '#157F3E']
    cmap = ListedColormap(verde)

    # Crear mapa de calor para zonas boscosas
    fig, ax = plt.subplots()
    im = ax.imshow(boscoso, cmap=cmap)

    # Añadir leyenda
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Zonas boscosas", rotation=-90, va="bottom")

    # Mostrar mapa de calor
    plt.show()

def crear_mapa_de_calor_vial():
    ## Generar matriz aleatoria de 100x100 con valores entre 0 y 1
    vial = np.random.rand(100, 100)

    # Convertir matriz aleatoria en infraestructura vial utilizando función sigmoidal
    vial = 1 / (1 + np.exp(-10*(vial-0.5)))

    # Crear paleta de colores para infraestructura vial
    gris = ['#F2F2F2', '#B2B2B2', '#595959', '#1A1A1A']
    cmap = ListedColormap(gris)

    # Crear mapa de calor para infraestructura vial
    fig, ax = plt.subplots()
    im = ax.imshow(vial, cmap=cmap)

    # Añadir leyenda
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Infraestructura vial", rotation=-90, va="bottom")

    # Mostrar mapa de calor
    plt.show()


