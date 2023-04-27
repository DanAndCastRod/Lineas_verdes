import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import noise
import math

def mostrar_mapas(mapas, cmap):
    n = int(np.ceil(np.sqrt(len(mapas)))) # calcular el tamaño del grid
    fig, axs = plt.subplots(n, n, figsize=(10, 10)) # crear la figura y los ejes
    axs = axs.flatten() # aplanar los ejes para iterar sobre ellos

    for i, mapa in enumerate(mapas):
        im = axs[i].imshow(mapa, cmap=cmap) # mostrar el mapa en el eje correspondiente
        axs[i].set_title(f"Mapa {i+1}") # establecer el título del eje
        fig.colorbar(im, ax=axs[i]) # agregar la barra de color al eje

    # eliminar los ejes vacíos del grid
    for i in range(len(mapas), n*n):
        fig.delaxes(axs[i])

    fig.tight_layout() # ajustar el diseño de la figura
    plt.show() # mostrar la figura

def mostrar_mapa( mapa, cmap):
    fig, ax = plt.subplots()
    im = ax.imshow(mapa, cmap=cmap)
    im.figure.colorbar(im)

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

def crear_microzonas(world, shape, sensibility):
    microzonas = np.zeros(shape)
    cmap_microzonas = ListedColormap(['#000','#fff',"#ff0000","#0f0"])
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i,j] > sensibility or world[i,j] < -sensibility :
                microzonas[i,j] = 0
            else: microzonas[i,j] = 1

    for i in range(100):
        randomcoor = (np.random.randint(0,shape[0]),np.random.randint(0,shape[1]/2))
        if microzonas[randomcoor] == 1:
            microzonas[randomcoor] =2
            break

    for i in range(100):
        randomcoor = (np.random.randint(0,shape[0]),np.random.randint(shape[1]/2,shape[1]))
        if microzonas[randomcoor] == 1:
            microzonas[randomcoor] =3
            break
    return microzonas, cmap_microzonas

def crear_pendientes(world, microzonas):
    shape = world.shape

    # Crear paleta de colores para relieve
    marron = ['#fff','#603813', '#965927', '#B5874E', '#CEAA7B','#E7CBA9' ]
    marron = ['#fff','#E7CBA9','#B5874E','#603813' ]
    cmap = ListedColormap(marron)
    
    tamanio_ventana = 1
    aux = np.zeros(shape)
    relieves = np.zeros(shape)
    # Recorrer la matriz y calcular el promedio de los puntos alrededor de cada punto
    for fila in range(tamanio_ventana // 2, world.shape[0] - tamanio_ventana // 2):
        for columna in range(tamanio_ventana // 2, world.shape[1] - tamanio_ventana // 2):
            ventana = world[fila - tamanio_ventana // 2 : fila + tamanio_ventana // 2 + 1, 
                            columna - tamanio_ventana // 2 : columna + tamanio_ventana // 2 + 1]
            if microzonas[fila,columna] == 1:
                aux[fila,columna] = np.mean(ventana)
            else:
                aux[fila,columna] = -1
    # n = 5
    # for i in range(n):
    #     quantil = 1/(i+1)
    #     for j in range(shape[0]):
    #         for k in range(shape[1]):
    #             if np.abs(aux[j,k]) <= quantil:
    #                 relieves[j,k] = i+1
            
    
    for i in range(shape[0]):
        for j in range(shape[1]):
            if np.abs(aux[i,j])<1 and microzonas[i,j] ==1:
                relieves[i,j] = 1
            if np.abs(aux[i,j])<0.3 and microzonas[i,j] ==1:
                relieves[i,j] = 2
            if np.abs(aux[i,j])<0.1  and microzonas[i,j] ==1:
                relieves[i,j] = 3
    
    return relieves, cmap

def crear_hidrico(world, microzonas):
    shape = world.shape


    azul = ['#fff', '#2674FF','#A4C8FF','#D7EFFF']#, '#0045B5']

    cmap = ListedColormap(azul)

    hidrico = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i,j]>-1 and world[i,j]<-0.6 and microzonas[i,j] ==1:
                hidrico[i,j] = 1
            elif world[i,j]>-0.75 and world[i,j]<-0.4 and microzonas[i,j] ==1:
                hidrico[i,j] = 2
            elif world[i,j]>-0.5 and world[i,j]<=0 and microzonas[i,j] ==1:
                hidrico[i,j] = 3
    
    return hidrico, cmap

def crear_bosques(world, microzonas):

    shape = world.shape
    # Crear paleta de colores para zonas boscosas
    verde = ['#fff','#C7EA46', '#9ED14A', '#6FBF4A', '#4DAF4A', '#2D9440', '#157F3E']
    verde = ['#fff','#157F3E','#4DAF4A','#9ED14A']
    cmap = ListedColormap(verde)
    bosques = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i,j]>0.5 and world[i,j]<0.6 and microzonas[i,j] ==1:
                bosques[i,j] = 1
            elif world[i,j]>0.45 and world[i,j]<0.7 and microzonas[i,j] ==1:
                bosques[i,j] = 2
            elif world[i,j]>0.05 and world[i,j]<0.8 and microzonas[i,j] ==1:
                
                bosques[i,j] = 3
    
    return bosques, cmap

def crear_vial(world, microzonas,window):
    shape = world.shape


    cmap = ListedColormap(["#fff","#ddd","#ccc","#bbb","#aaa"])
    vial_map = np.zeros(shape)
    

    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i,j] >0.5 and world[i,j] < 0.51 and microzonas[i,j]==1:
                vial_map[i,j] = 1
            elif world[i,j] >0.5 and world[i,j] < 0.52 and microzonas[i,j]==1:
                vial_map[i,j] = 2
            elif world[i,j] >0.5 and world[i,j] < 0.53 and microzonas[i,j]==1:
                vial_map[i,j] = 3
            elif world[i,j] >0.5 and world[i,j] < 0.55 and microzonas[i,j]==1:
                vial_map[i,j] = 4
            else:
                vial_map[i,j] = 0
                
    tamanio_ventana = window
    aux = np.zeros(shape)

    # Recorrer la matriz y calcular el promedio de los puntos alrededor de cada punto
    for fila in range(tamanio_ventana // 2, vial_map.shape[0] - tamanio_ventana // 2):
        for columna in range(tamanio_ventana // 2, vial_map.shape[1] - tamanio_ventana // 2):
            ventana = vial_map[fila - tamanio_ventana // 2 : fila + tamanio_ventana // 2 + 1, 
                            columna - tamanio_ventana // 2 : columna + tamanio_ventana // 2 + 1]
            aux[fila,columna] = np.mean(ventana)
    vial2 = aux
    return vial2, cmap

def print_zeros(n):
    for i in range(n):
        print(0)
