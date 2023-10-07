#%%
import mapping as mp
import pandas as pd
def read_sheet(filename, sheetname):
    df = pd.read_excel(filename, sheet_name=sheetname, header=None)
    return df
filename = '/root/.node-red/public/Lineas_verdes/dijkstra V1 (2)/dijkstra V1/mapa7.xlsx'


world = mp.generar_mundo(100,100,30,8,0.5,2,2013)
zacti,cmap_acti = mp.crear_microzonas(world, (100,100), 0.8)

_,cmap_hidr = mp.crear_hidrico(world,zacti)
_,cmap_pend = mp.crear_pendientes(world,zacti)
_,cmap_bosq = mp.crear_bosques(world,zacti)
_,cmap_vial = mp.crear_vial(world,zacti,1)
ZonasActivas = 'acti'
ZonasBosque = 'bosq'
ZonasPendiente = 'pend'
ZonasHidr = 'hidr'
ZonasVias = 'vias'
world = read_sheet(filename, 'world').values
Zacti = read_sheet(filename, ZonasActivas).values
Zbosq = read_sheet(filename, ZonasBosque).values
Zpend = read_sheet(filename, ZonasPendiente).values
Zhidr = read_sheet(filename, ZonasHidr).values
Zvias = read_sheet(filename, ZonasVias).values
mp.mostrar_mapa(world, 'terrain')
mp.mostrar_mapa(Zacti,cmap_acti)
mp.mostrar_mapa(Zbosq,cmap_bosq)
mp.mostrar_mapa(Zpend,cmap_pend)
mp.mostrar_mapa(Zhidr,cmap_hidr)
mp.mostrar_mapa(Zvias,cmap_vial)
print("OK")
# %%
