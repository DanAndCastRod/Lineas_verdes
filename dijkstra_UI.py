
import numpy as np
from mapping import generar_mundo
from mapping import crear_bosques
from mapping import crear_hidrico
from mapping import crear_microzonas
from mapping import crear_pendientes
from mapping import crear_vial
from mapping import mostrar_mapa
from mapping import mostrar_mapa_new_1
import pandas as pd
from Dijkstra_module import dijkstra
from math import sqrt
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import pandas as pd


def main():
    sg.theme('DefaultNoMoreNagging')  # Aplica un tema predefinido

    layout = [
        [sg.Text('Seleccione un archivo')],
        [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse()],
        [sg.Button('Cargar', button_color=('white', '#007bff')),
         sg.Button('Salir', button_color=('white', '#dc3545'))],
        [sg.Text('Resultados:')],
        [sg.Output(size=(80, 20), key='-OUTPUT-')],
        [sg.Canvas(key='-CANVAS-')]  # Espacio para mostrar la gráfica
    ]

    window = sg.Window('Interfaz de carga de archivos', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break

        if event == 'Cargar':
            filename = values['-FILE-']
            if filename:
                process_file(filename)
                # Llama a la función para mostrar la gráfica

    window.close()


def process_file(filename):
    try:
   
        print("========== 0%")
        # Micro áreas
        h = 1  # alto km
        w = 1  # ancho km

        # tamaño de la zona en áreas
        H = 100  # alto km
        W = 100  # ancho km

        shape = np.array((H, W))
        scale = (H*w + W*h)/(2*w*h)

        # Costos
        """
        Se contemplan los costos en unidades $/km
        Sobre este costo operan los siguientes factores
        """

        costo_bosque = 100000  # US$/km
        costo_pendiente = 100000  # US$/km
        costo_distancia = 100000  # US$/km
        costo_vias = 100000  # US$/km
        costo_hidrico = 100000  # US$/km

        world = generar_mundo(H, W, scale, 6, 0.5, 2.0, 2023)
        Zacti, cmap_acti = crear_microzonas(world, shape, 0.55)
        # Zbosq, cmap_bosq = crear_bosques(world, Zacti)
        # Zpend, cmap_pend = crear_pendientes(world, Zacti)
        # Zhidr, cmap_hidr = crear_hidrico(world, Zacti)
        # Zvias, cmap_vias = crear_vial(world, Zacti, 1)

        # Zacti = Zacti.astype(int)
        # Zbosq = Zbosq.astype(int)
        # Zpend = Zpend.astype(int)
        # Zhidr = Zhidr.astype(int)
        # Zvias = Zvias.astype(int)
        # np.unique(Zvias)
        def read_sheet(filename, sheetname):
            df = pd.read_excel(filename, sheet_name=sheetname, header=None)
            return df
        Zonaworld = 'world'
        world = read_sheet(filename, Zonaworld).values
        ZonasActivas = 'acti'
        Zacti = read_sheet(filename, ZonasActivas).values
        ZonasBosque = 'bosq'
        Zbosq = read_sheet(filename, ZonasBosque).values
        ZonasPendiente = 'pend'
        Zpend = read_sheet(filename, ZonasPendiente).values
        ZonasHidr = 'hidr'
        Zhidr = read_sheet(filename, ZonasHidr).values

        ZonasVias = 'vias'
        Zvias = read_sheet(filename, ZonasVias).values


        FCost_Zbosq = np.array([1, 1, 0.5, 0.3])
        FCost_Zvia = np.array([1, 1, 0.5, 0.8, 2, 4])
        FCost_Zpend = np.array([1, 1, 0.3, 0.2])
        FCost_Zhidr = np.array([1, 1, 0.5, 0.2])
        SCI = FCost_Zbosq[Zbosq]*costo_bosque + FCost_Zvia[Zvias]*costo_vias + FCost_Zhidr[Zhidr]*costo_hidrico + FCost_Zpend[Zpend]*costo_pendiente

        (rows, cols) = np.where(Zacti)
        pos = np.flatnonzero(Zacti)
        NumMicroAreas = pos.size
        NumColumnas = W//w
        NumFilas = H//h

        MapaMicroAreaActiva = np.column_stack(
            (np.arange(0, NumMicroAreas), pos, rows, cols))
        MicroArea_Ini = np.flatnonzero(Zacti == 2)
        MicroArea_fin = np.flatnonzero(Zacti == 3)

        PuntoIni = np.flatnonzero(MapaMicroAreaActiva[:, 1] == MicroArea_Ini[0])
        PuntoFin = np.flatnonzero(MapaMicroAreaActiva[:, 1] == MicroArea_fin[0])

        MapaVecinosMicroAreas = np.zeros((NumMicroAreas, 8), dtype=int)
        MapaVecinoDiagonales = np.zeros((NumMicroAreas, 8), dtype=int)

        for i in range(NumMicroAreas):
            X = MapaMicroAreaActiva[i, 1]
            ConsiderarLimitesAbajo = True
            ConsiderarLimitesArriba = True
            if MapaMicroAreaActiva[i, 2] == NumFilas - 1:
                ConsiderarLimitesAbajo = True
            if MapaMicroAreaActiva[i, 2] == 0:
                ConsiderarLimitesArriba = True

            contador = 0
            cont_i = -1
            Lim_m = 3
            Lim_n = 3
            for m in range(Lim_m):
                if ConsiderarLimitesArriba:
                    Vecino = X+cont_i*NumFilas
                    Lim_n = 2

                else:
                    Vecino = X+cont_i*NumFilas-1

                cont_i = cont_i+1
                cont_j = 0

                if ConsiderarLimitesAbajo:
                    Lim_n = 2
                for n in range(Lim_n):
                    Vecino = Vecino+cont_j
                    cont_j = 1
                    if Vecino != X:
                        PosVecino = np.flatnonzero(MapaMicroAreaActiva[:, 1] == Vecino)
                        if PosVecino.size != 0:
                            contador = contador + 1
                            if (m == 0 and n == 0) or (m == 0 and n == 2) or (m == 2 and n == 0) or (m == 2 and n == 2):
                                MapaVecinoDiagonales[i, contador-1] = 1
                            elif (m == 0 and n == 1) or (m == 2 and n == 1):
                                MapaVecinoDiagonales[i, contador-1] = 2
                            else:
                                MapaVecinoDiagonales[i, contador-1] = 3

                            MapaVecinosMicroAreas[i, contador-1] = PosVecino[0]

        AdyPonderaciones = np.zeros((NumMicroAreas, NumMicroAreas))

        for MicroArea in range(NumMicroAreas):
            for v in range(8):
                Vecino = MapaVecinosMicroAreas[MicroArea, v]
                if Vecino == 0:
                    break

                if MapaVecinoDiagonales[MicroArea, v] == 1:
                    FDistancia = sqrt(h**2+w**2)
                elif MapaVecinoDiagonales[MicroArea, v] == 2:
                    FDistancia = w
                elif MapaVecinoDiagonales[MicroArea, v] == 3:
                    FDistancia = h
                CostoTramoDistancia = costo_distancia*FDistancia

                TipoBosqueMicroArea_i = Zbosq.flat[MapaMicroAreaActiva[MicroArea, 1]]

                Fbosque_i = 0 if TipoBosqueMicroArea_i == 0 else FCost_Zbosq[TipoBosqueMicroArea_i-1]
                TipoBosqueMicroArea_j = Zbosq.flat[MapaMicroAreaActiva[Vecino, 1]]
                Fbosque_j = 0 if TipoBosqueMicroArea_j == 0 else FCost_Zbosq[TipoBosqueMicroArea_j-1]
                CostoTramoBosque = (Fbosque_i+Fbosque_j)*FDistancia/2*costo_bosque

                TipoViaMicroArea_i = Zvias.flat[MapaMicroAreaActiva[MicroArea, 1]]
                Fvia_i = 0 if TipoViaMicroArea_i == 0 else FCost_Zvia[TipoViaMicroArea_i-1]
                TipoViaMicroArea_j = Zvias.flat[MapaMicroAreaActiva[Vecino, 1]]
                Fvia_j = 0 if TipoViaMicroArea_j == 0 else FCost_Zvia[TipoViaMicroArea_j-1]
                CostoTramoVia = (Fvia_i+Fvia_j)*FDistancia/2*costo_vias

                TipoPendMicroArea_i = Zpend.flat[MapaMicroAreaActiva[MicroArea, 1]]
                Fpend_i = 0 if TipoPendMicroArea_i == 0 else FCost_Zpend[TipoPendMicroArea_i-1]
                TipoPendMicroArea_j = Zpend.flat[MapaMicroAreaActiva[Vecino, 1]]
                Fpend_j = 0 if TipoPendMicroArea_j == 0 else FCost_Zpend[TipoPendMicroArea_j-1]
                CostoTramoPendiente = (Fpend_i+Fpend_j)*FDistancia/2*costo_pendiente

                TipoHidricoMicroArea_i = Zhidr.flat[MapaMicroAreaActiva[MicroArea, 1]]
                Fhidr_i = 0 if TipoHidricoMicroArea_i == 0 else FCost_Zhidr[TipoHidricoMicroArea_i-1]
                TipoHidricoMicroArea_j = Zhidr.flat[MapaMicroAreaActiva[Vecino, 1]]
                Fhidr_j = 0 if TipoHidricoMicroArea_j == 0 else FCost_Zhidr[TipoHidricoMicroArea_j-1]
                CostoTramoHidrico = (Fhidr_i+Fhidr_j)*FDistancia/2*costo_hidrico

                AdyPonderaciones[MicroArea, Vecino] = CostoTramoDistancia + \
                    CostoTramoBosque + CostoTramoPendiente + CostoTramoVia + CostoTramoHidrico


        import time
        def run_model():
            print("****====== 40%")
            start_time = time.time()
            
            [e,L] = dijkstra(AdyPonderaciones,PuntoIni[0],PuntoFin[0])
            dur = time.time() - start_time
            mapa_sol = np.zeros_like(world)
            return dur, mapa_sol, e,L
        [dur, mapa_sol, e, L] = run_model()
        # Luego, tomamos cada índice en la lista L
        for index in L:
            print("******==== 60%")
            # Buscamos las coordenadas correspondientes a este índice en las celdas activas
            coord = np.where(MapaMicroAreaActiva[:,0] == index)

            # si la celda activa fue encontrada
            if coord[0].size > 0:
                row = MapaMicroAreaActiva[coord[0][0], 2]
                col = MapaMicroAreaActiva[coord[0][0], 3]

                # Marcamos estas coordenadas en el mapa de la solución
                mapa_sol[row, col] = 1000000000
        print("********** 100%")
        print(f"El modelo tardó: {round(dur,2)} sg En solucionar")





        # Finalmente, mostramos el mapa de la solución
        from mapping import mostrar_mapa_new_1, mostrar_mapa
        mostrar_mapa(Zacti,cmap_acti)
        mostrar_mapa_new_1(SCI, 'hot',mapa_sol)
        mostrar_mapa_new_1(world, 'terrain', mapa_sol)

    except Exception as e:
        print(f'Error al procesar el archivo: {e}')




if __name__ == '__main__':
    main()
