import PySimpleGUI as sg
import matplotlib.pyplot as plt
import pandas as pd
from mapping import mostrar_mapa_new
import mapping as mp
import numpy as np
# Micro áreas
h = 1  # alto km
w = 1  # ancho km

# tamaño de la zona en áreas
H = 100  # alto km
W = 100  # ancho km
costo_bosque = 100000  # US$/km
costo_pendiente = 100000  # US$/km
costo_distancia = 100000  # US$/km
costo_vias = 100000  # US$/km
costo_hidrico = 100000  # US$/km
shape = np.array((H, W))
scale = (H*w + W*h)/(2*w*h)
world = mp.generar_mundo(H, W, scale, 6, 0.5, 2.0, 2023)
Zacti, cmap_acti = mp.crear_microzonas(world, shape, 0.55)
Zbosq, cmap_bosq = mp.crear_bosques(world, Zacti)
Zpend, cmap_pend = mp.crear_pendientes(world, Zacti)
Zhidr, cmap_hidr = mp.crear_hidrico(world, Zacti)
Zvias, cmap_vias = mp.crear_vial(world, Zacti, 1)

def main():
    sg.theme('DefaultNoMoreNagging')  # Aplica un tema predefinido

    layout = [
        [sg.Text('Seleccione un archivo')],
        [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse()],
        [sg.Button('Cargar', button_color=('white', '#007bff')), sg.Button('Salir', button_color=('white', '#dc3545'))],
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
                plot_chart(filename)  # Llama a la función para mostrar la gráfica

    window.close()

def process_file(filename):
    try:
        
        data = pd.read_excel(filename)
        
        def read_sheet(filename, sheetname):
            df = pd.read_excel(filename, sheet_name=sheetname, header=None)
            return df




        ZonasActivas = 'acti'
        Zacti = read_sheet(filename, ZonasActivas).values
        ZonasBosque = 'bosq'
        Zbosq = read_sheet(filename, ZonasBosque).values
        ZonasPendiente = 'pend'
        Zpend = read_sheet(filename, ZonasPendiente).values
        ZonasHidrico = 'hidr'
        Zhidr = read_sheet(filename, ZonasHidrico).values
        ZonasVias = 'vias'
        Zvias = read_sheet(filename, ZonasVias).values
        


        
        # with open(filename, 'r') as file:
        #     content = file.read()
        #     print(content)
    except Exception as e:
        print(f'Error al procesar el archivo: {e}')

def plot_chart(filename):
    try:
        df = pd.read_excel(filename)  # Lee el archivo CSV utilizando pandas

        mp.mostrar_mapa(world, "terrain")
    except Exception as e:
        print(f'Error al mostrar la gráfica: {e}')

if __name__ == '__main__':
    main()
