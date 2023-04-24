import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import noise

def generar_mundo(n,m,scale, octaves, persistance, lacunarity, seed):
    shape = (n,m)
    scale = scale
    octaves = octaves
    persistance = persistance
    lacunarity = lacunarity
    seed = seed
    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i,j] = noise.pnoise2(
                i/scale,
                j/scale,
                octaves = octaves,
                persistence = persistance,
                lacunarity = lacunarity,
                base = seed
            )


    world = world/(np.max(world)- np.min(world))*2
    return world
    

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




def microzonas(world, shape, sensibility):
    microzonas = np.zeros(shape)
    cmap_microzonas = ListedColormap(['#000','#fff',"#ff0000","#0f0"])
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i,j] > sensibility or world[i,j] < -sensibility :
                microzonas[i,j] = 0
            else: microzonas[i,j] = 1

    for i in range(100):
        randomcoor = (np.random.randint(0,shape[0]),np.random.randint(0,shape[1]))
        if microzonas[randomcoor] == 1:
            microzonas[randomcoor] =2
            break

    for i in range(100):
        randomcoor = (np.random.randint(0,shape[0]),np.random.randint(0,shape[1]))
        if microzonas[randomcoor] == 1:
            microzonas[randomcoor] =3
            break
    return microzonas, cmap_microzonas

def print_zeros(n):
    for i in range(n):
        print(0)
    
def mostrar_mapa( mapa, cmap):
    fig, ax = plt.subplots()
    im = ax.imshow(mapa, cmap=cmap)
    im.figure.colorbar(im)

