# Sistema de información
# Diseño óptimo de ruta para línea de transmisión
import numpy as np
from mapping import generar_mundo
from mapping import crear_bosques
from mapping import crear_hidrico
from mapping import crear_microzonas
from mapping import crear_pendientes
from mapping import crear_vial


# Micro áreas
h = 1 # alto km
w = 1 # ancho km

# tamaño de la zona en áreas 
H = 100 # alto km
W = 100 # ancho km

shape = np.array((H,W))
scale = (H*w + W*h)/(2*w*h)

# Costos
"""
Se contemplan los costos en unidades $/km 
Sobre este costo operan los siguientes factores
"""
costo_bosque =      100000  # US$/km
costo_pendiente =   100000  # US$/km
costo_distancia =   100000  # US$/km
costo_vias =        100000  # US$/km
costo_hidrico =     100000  # US$/km

world = generar_mundo(H, W, scale, 6, 0.5, 2.0,2023)
zacti,cmap_acti = crear_microzonas(world, shape, 0.55)
zbosq,cmap_bosq = crear_bosques(world, zacti)
zpend,cmap_pend = crear_pendientes(world, zacti)
zhidr,cmap_hidr = crear_hidrico(world, zacti)
zvias,cmap_vias = crear_vial(world, zacti,1)


