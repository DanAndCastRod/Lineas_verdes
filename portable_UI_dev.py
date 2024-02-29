#%%
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mapping as mp
from tkinter import ttk
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
import time
#%%
class DijkstraApp:

    def __init__(self,root):
        self.root = root
        self.root.title("Dijkstra Aplication")
        self.root.geometry("800x600")

        self.filename = None
        self.df = None
        self.menu = tk.Menu(self.root)
        self.root.config(menu = self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label = "Archivo", menu=self.file_menu)
        self.frame = tk.Frame(self.root)
        self.frame.pack(side = tk.TOP, anchor=tk.W, pady=(5,0), padx=(5,0))
        self.file_menu.add_command(label="Abrir", command = self.load_file)
        self.file_menu.add_command(label="Guardar como...", command = self.save_file, state="disabled")
        self.load_button = tk.Button(self.frame, text = "Cargar archivo", command=self.load_file)
        self.load_button.pack(side = tk.LEFT, pady=(5,0))
        self.execute_button = tk.Button(self.frame, text = "Ejecutar", command = self.execute_dijkstra, state="disabled")
        self.execute_button.pack(side = tk.LEFT, pady = (5,0), padx=(5,0))
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill = tk.BOTH, expand=1)

        self.status_label = tk.Label(self.root, text = "Carga el archivo xlsx para comenzar", bd = 1 , relief=tk.SUNKEN, anchor = tk.W)
        self.status_label.pack(side = tk.BOTTOM, fill = tk.X)

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Excel files","*.xlsx")])
        if not self.filename:
            return
        try:
            self.df = pd.read_excel(self.filename, sheet_name="world")
        except Exception as e:
            messagebox.showerror("Error", f"error al cargar el archivo:{e}")
            return

        self.show_data()
        self.file_menu.entryconfig("Guardar como...", state = "normal")
        self.execute_button.configure(state="normal")
        self.status_label.config(text = f"{self.filename} cargado")

    def show_data(self):
        if self.df is None:
            messagebox.showinfo("Información", "No hay datos para mostrar")
            return
        if not (self.df.select_dtypes(include=[int,float]).shape== self.df.shape):
            messagebox.showwarning("Advertencia", "El Dataframe contiene datos no numéricos")
        fig, ax = plt.subplots(figsize = (8,6))
        plot,ax = mp.mostrar_mapa(self.df, "terrain")
        try:
            self.chart.get_tk_widget().pack_forget()
        except: pass
        self.chart = FigureCanvasTkAgg(plot, self.canvas_frame)
        self.chart.get_tk_widget().pack(fill = tk.BOTH, expand=1)

    
    def execute_dijkstra(self):
        print("ejecutando")
        ## Barra de progreso
        self.progress = ttk.Progressbar(self.canvas_frame, orient="horizontal",
                                        length=400, mode="determinate")
        self.progress.pack(side=tk.TOP, pady=(10, 0))

        # self.infoframe = tk.Frame(self.root)
        self.chart.get_tk_widget().pack_forget()
        self.inform = tk.Label(self.canvas_frame, text="Ejecutando...", )
        self.inform.pack(side = tk.TOP, fill=tk.X, anchor=tk.W)
  
        self.progress["value"] = 10
        self.inform.config(text="Definiendo parametros")
        h = 1 
        w = 1 
        H = 100
        W = 100
        self.progress["value"] = 20
        self.root.update_idletasks()
        shape = np.array((H,W))
        scale= (H*w+W*h)/(2*w*h)


        self.inform.config(text="Calculando superficie de costos")
        
        ## Costos
        costo_bosque = 100000
        costo_pendiente = 100000
        costo_distancia = 100000
        costo_vias = 1000000
        costo_hidrico = 100000

        world = generar_mundo(H,W, scale, 6, 0.5,2.0,2023)
        Zacti, cmap_acti = crear_microzonas(world, shape, 0.55)
        def read_sheet(filename,sheetname):
            df = pd.read_excel(filename, sheet_name=sheetname, header = None)
            return df
        
        self.world = read_sheet(self.filename, "world").values
        ZonasActivas = 'acti'
        self.Zacti = read_sheet(self.filename, ZonasActivas).values
        ZonasBosque = 'bosq'
        self.Zbosq = read_sheet(self.filename, ZonasBosque).values
        ZonasPendiente = 'pend'
        self.Zpend = read_sheet(self.filename, ZonasPendiente).values
        ZonasHidr = 'hidr'
        self.Zhidr = read_sheet(self.filename, ZonasHidr).values
        ZonasVias = 'vias'
        self.Zvias = read_sheet(self.filename, ZonasVias).values
        _, cmap_acti = crear_microzonas(self.world, shape, 0.55)
        _, cm_bosq = crear_bosques(self.world, self.Zacti)
        _, cm_pend = crear_pendientes(self.world,self.Zacti)
        _, cm_hidr = mp.crear_hidrico(self.world, self.Zacti)
        _, cm_vias = mp.crear_vial(self.world, self.Zacti,2)
        fig, ax = plt.subplots(2,3,layout ="constrained")
        mp.mostrar_mapa2(ax[0,0],self.world, "terrain")
        mp.mostrar_mapa2(ax[0,1],self.Zacti, cmap_acti)
        mp.mostrar_mapa2(ax[0,2],self.Zbosq, cm_bosq)
        mp.mostrar_mapa2(ax[1,0],self.Zpend, cm_pend)
        mp.mostrar_mapa2(ax[1,1],self.Zhidr, cm_hidr)
        mp.mostrar_mapa2(ax[1,2],self.Zvias, cm_vias)
        plot = fig
        self.chart = FigureCanvasTkAgg(plot, self.canvas_frame)
        self.chart.get_tk_widget().pack(fill = tk.BOTH, expand=1)
        FCost_Zbosq = np.array([1, 1, 0.5, 0.3])
        FCost_Zvia = np.array([1, 1, 0.5, 0.8, 2, 4])
        FCost_Zpend = np.array([1, 1, 0.3, 0.2])
        FCost_Zhidr = np.array([1, 1, 0.5, 0.2])
        self.SCI = FCost_Zbosq[self.Zbosq]*costo_bosque+FCost_Zvia[self.Zvias]*costo_vias+FCost_Zpend[self.Zpend]*costo_pendiente+FCost_Zhidr[self.Zhidr]*costo_hidrico
        self.inform.config(text="Calculando Mapa de vecinos")
        self.progress["value"] = 30
        self.root.update_idletasks()
        (rows, cols) = np.where(self.Zacti)
        pos = np.flatnonzero(self.Zacti)
        NumMicroAreas = pos.size
        NumColumnas = W//W
        NumFilas = H//h

        MapaMicroAreaActiva = np.column_stack(
            (np.arange(0,NumMicroAreas), pos, rows, cols)
        )       
        MicroArea_ini = np.flatnonzero(self.Zacti == 2)
        MicroArea_fin = np.flatnonzero(self.Zacti == 3)

        PuntoIni = np.flatnonzero(MapaMicroAreaActiva[:,1] == MicroArea_ini[0])
        PuntoFin = np.flatnonzero(MapaMicroAreaActiva[:,1] == MicroArea_fin[0])

        MapaVecinosMicroAreas = np.zeros((NumMicroAreas, 8), dtype=int)
        MapaVecinosDiagonales = np.zeros((NumMicroAreas, 8), dtype=int)
        inc = 0
        for i in range(NumMicroAreas):
            X = MapaMicroAreaActiva[i,1]
            ConsiderarLimitesAbajo = True
            ConsiderarLimitesArriba = True
            if MapaMicroAreaActiva[i, 2] == NumFilas -1:
                ConsiderarLimitesAbajo = True
            if MapaMicroAreaActiva[i, 2] == 0:
                ConsiderarLimitesArriba = True

            contador = 0
            cont_i = -1
            Lim_m = 3
            Lim_n = 3
            for m in range(Lim_m):
                if ConsiderarLimitesArriba:
                    Vecino = X + cont_i*NumFilas
                    Lim_n = 2
                else:
                    Vecino = X + cont_i*NumFilas -1
                cont_i = cont_i+1
                cont_j = 0

                if ConsiderarLimitesAbajo:
                    Lim_n = 2
                for n in range(Lim_n):
                
                    inc += 100/(NumMicroAreas*Lim_m*Lim_n)
                    self.progress["value"] = inc
                    self.root.update_idletasks()
                    Vecino = Vecino+cont_j
                    cont_j = 1
                    if Vecino != X:
                        PosVecino = np.flatnonzero(MapaMicroAreaActiva[:,1] == Vecino)
                        if PosVecino.size != 0:
                            contador = contador + 1
                            if(m == 0 and n == 0) or (m == 0 and n == 2) or (m == 2 and n == 0) or (m == 2 and n == 2):
                                MapaVecinosDiagonales[i, contador - 1] = 1
                            elif(m == 0 and n == 1) or (m==2 and n == 1):
                                MapaVecinosDiagonales[i, contador - 1] = 2
                            else:
                                MapaVecinosDiagonales[i, contador - 1] = 3
                            
                            MapaVecinosMicroAreas[i, contador - 1] = PosVecino[0]
        self.AdyPonderaciones = np.zeros((NumMicroAreas, NumMicroAreas))
        self.inform.config(text="Calculando Costo por MicroArea")
        inc = 0
        for MicroArea in range(NumMicroAreas):
            # print(inc)
            inc += 100/(NumMicroAreas)
            
            self.progress["value"] = inc
            self.root.update_idletasks()
            for v in range(8):

                Vecino = MapaVecinosMicroAreas[MicroArea, v]
                if Vecino == 0: break

                if MapaVecinosDiagonales[MicroArea, v] == 1:
                    FDistancia = sqrt(h**2 + w**2)
                elif MapaVecinosDiagonales[MicroArea, v] == 2:
                    FDistancia = w
                elif MapaVecinosDiagonales[MicroArea, v] == 3:
                    FDistancia = h
                CostoTramoDistancia = costo_distancia*FDistancia

                TipoBosqueMicroArea_i = self.Zbosq.flat[MapaMicroAreaActiva[MicroArea, 1]]

                Fbosque_i = 0 if TipoBosqueMicroArea_i == 0 else FCost_Zbosq[TipoBosqueMicroArea_i-1]
                
                TipoBosqueMicroArea_j = self.Zbosq.flat[MapaMicroAreaActiva[Vecino, 1]]
                
                Fbosque_j = 0 if TipoBosqueMicroArea_j == 0 else FCost_Zbosq[TipoBosqueMicroArea_j-1]

                CostoTramoBosque = (Fbosque_i+Fbosque_j) * FDistancia / 2 * costo_bosque

                
                TipoViaMicroArea_i = self.Zvias.flat[MapaMicroAreaActiva[MicroArea, 1]]
                
                Fvia_i = 0 if TipoViaMicroArea_i == 0 else FCost_Zvia[TipoViaMicroArea_i-1]
                
                TipoViaMicroArea_j = self.Zvias.flat[MapaMicroAreaActiva[Vecino, 1]]
                
                Fvia_j = 0 if TipoViaMicroArea_j == 0 else FCost_Zvia[TipoViaMicroArea_j-1]
                
                CostoTramoVia = (Fvia_i+Fvia_j)*FDistancia/2*costo_vias


                
                TipoPendMicroArea_i = self.Zpend.flat[MapaMicroAreaActiva[MicroArea, 1]]
                
                Fpend_i = 0 if TipoPendMicroArea_i == 0 else FCost_Zpend[TipoPendMicroArea_i-1]
                
                TipoPendMicroArea_j = self.Zpend.flat[MapaMicroAreaActiva[Vecino, 1]]
                
                Fpend_j = 0 if TipoPendMicroArea_j == 0 else FCost_Zpend[TipoPendMicroArea_j-1]
                
                CostoTramoPendiente = (Fpend_i+Fpend_j)*FDistancia/2*costo_pendiente


                
                TipoHidricoMicroArea_i = self.Zhidr.flat[MapaMicroAreaActiva[MicroArea, 1]]
                
                Fhidr_i = 0 if TipoHidricoMicroArea_i == 0 else FCost_Zhidr[TipoHidricoMicroArea_i-1]
                
                TipoHidricoMicroArea_j = self.Zhidr.flat[MapaMicroAreaActiva[Vecino, 1]]
                
                Fhidr_j = 0 if TipoHidricoMicroArea_j == 0 else FCost_Zhidr[TipoHidricoMicroArea_j-1]
                
                CostoTramoHidrico = (Fhidr_i+Fhidr_j)*FDistancia/2*costo_hidrico

                
                self.AdyPonderaciones[MicroArea, Vecino] = CostoTramoDistancia + \
                    CostoTramoBosque + CostoTramoPendiente + CostoTramoVia + CostoTramoHidrico
        
        
        self.inform.config(text="Ejecutando modelo")
        inc = 30
        self.progress["value"] = inc
        self.root.update_idletasks()
        def run_model():
            self.progress["value"] = 60
            self.root.update_idletasks()
            starttime = time.time()
            [e, L] = dijkstra(self.AdyPonderaciones, PuntoIni[0], PuntoFin[0])
            dur = time.time() - starttime
            map_sol = np.zeros_like(world)
            return dur, map_sol, e, L

        [dur, map_sol, e, L] = run_model()
        self.inform.config(text="Sobreescribiendo matriz de solución")

        # Pre-calcular incremento de progreso
        progress_increment = 100 / len(L)

        # Posiblemente preprocesar MapaMicroAreaActiva para un acceso más rápido
        # Por ejemplo, creando un diccionario si index es único
        # map_index_to_coords = {index: (row, col) for index, row, col in MapaMicroAreaActiva}

        for index in L:
            self.progress["value"] += progress_increment
            if len(L) > 100 and self.progress["value"] % 5 == 0:
                # Actualizar la interfaz de usuario cada 5% de progreso
                self.root.update_idletasks()

            coord = np.where(MapaMicroAreaActiva[:, 0] == index)

            if coord[0].size > 0:
                row = MapaMicroAreaActiva[coord[0][0], 2]
                col = MapaMicroAreaActiva[coord[0][0], 3]
                map_sol[row, col] = 10000

        # Considera actualizar la interfaz de usuario una vez después del bucle
        self.root.update_idletasks()

        self.chart.get_tk_widget().pack_forget()
        self.map_sol = pd.DataFrame(map_sol)

        self.status_label.config(text = f"Ejecución finalizada en {round(dur,2)} sg")
        self.download_button = tk.Button(self.frame, text = "Descargar Resultados", command=self.save_result)
        self.download_button.pack(side=tk.LEFT, pady = (5,0))
        # fig, ax = plt.subplots(2,3,layout ="constrained")
        mp.mostrar_mapa_new_2(ax[0,0],self.world, "terrain", map_sol,"")
        mp.mostrar_mapa_new_2(ax[0,1],self.Zacti, cmap_acti, map_sol,"")
        mp.mostrar_mapa_new_2(ax[0,2],self.Zbosq, cm_bosq, map_sol,"")
        mp.mostrar_mapa_new_2(ax[1,0],self.Zpend, cm_pend, map_sol,"")
        mp.mostrar_mapa_new_2(ax[1,1],self.Zhidr, cm_hidr, map_sol,"")
        mp.mostrar_mapa_new_2(ax[1,2],self.Zvias, cm_vias, map_sol,"")
        plot = fig
        self.chart = FigureCanvasTkAgg(plot, self.canvas_frame)
        self.chart.get_tk_widget().pack(fill = tk.BOTH, expand=1)

    def save_result(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if output_file:
            self.map_sol.to_excel(output_file)
            self.status_label.config(f"Guardado en {output_file}")
            # try:
            # except Exception as e:
            #     messagebox.showerror("Error", f"Error al guardar el archivo: {e}")


    def save_file(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files","*.xlsx")])
        if output_file:
            try:
                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                    self.df.to_excel(writer)
                self.status_label.config(f"Guardado en {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

if __name__ == "__main__":
    
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()
# %%
