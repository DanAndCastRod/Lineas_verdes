import PySimpleGUI as sg
import matplotlib.pyplot as plt
import pandas as pd

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
        # Aquí puedes agregar el código para procesar el archivo
        # En este ejemplo, simplemente se lee el contenido del archivo y se muestra en la salida
        with open(filename, 'r') as file:
            content = file.read()
            print(content)
    except Exception as e:
        print(f'Error al procesar el archivo: {e}')

def plot_chart(filename):
    try:
        df = pd.read_csv(filename)  # Lee el archivo CSV utilizando pandas
        df['valor'] = df['valor'].str.replace(',', '.').astype(float)  # Reemplaza las comas por puntos en la columna 'valor' y convierte a float
        avg_values = df.groupby('ID_itm')['valor'].std()/df.groupby('ID_itm')['valor'].mean()  # Calcula el valor promedio por ítem

        plt.figure(figsize=(8, 6))  # Configura el tamaño de la figura
        avg_values.plot(kind='bar', color='#007bff')  # Grafica los valores promedio como barras con color azul
        plt.xlabel('ID_itm')
        plt.ylabel('$\sigma/\mu$')
        plt.title('Valor promedio por ítem')
        plt.tight_layout()  # Ajusta el espaciado
        plt.show()
    except Exception as e:
        print(f'Error al mostrar la gráfica: {e}')

if __name__ == '__main__':
    main()
