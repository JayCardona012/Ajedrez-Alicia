import customtkinter as ctk
from tkinter import messagebox

# Clase para representar el tablero y sus piezas
class AjedrezAlicia:
    def __init__(self, root):
        self.root = root
        self.tablero_a = []
        self.tablero_b = []
        self.ocupacion_a = [[None for _ in range(8)] for _ in range(8)]  # Estado lógico del tablero A
        self.ocupacion_b = [[None for _ in range(8)] for _ in range(8)] 
        self.pieza_seleccionada = None
        self.tablero_actual = 'A'  # Para alternar entre tableros
        self.crear_tableros()

    def crear_tableros(self):
        self.frame_a = ctk.CTkFrame(self.root)
        self.frame_a.grid(row=0, column=0, padx=10, pady=10)
        
        self.frame_b = ctk.CTkFrame(self.root)
        self.frame_b.grid(row=0, column=1, padx=10, pady=10)

        # Crear tablero A
        for i in range(8):
            fila = []
            for j in range(8):
                casilla = ctk.CTkButton(self.frame_a, text="", width=40, height=40, 
                                        fg_color=("beige" if (i + j) % 2 == 0 else "brown"),
                                        command=lambda x=i, y=j: self.seleccionar_casilla(x, y, 'A'))
                casilla.grid(row=i, column=j)
                fila.append(casilla)
            self.tablero_a.append(fila)

        # Crear tablero B
        for i in range(8):
            fila = []
            for j in range(8):
                casilla = ctk.CTkButton(self.frame_b, text="", width=40, height=40, 
                                        fg_color=("beige" if (i + j) % 2 == 0 else "brown"),
                                        command=lambda x=i, y=j: self.seleccionar_casilla(x, y, 'B'))
                casilla.grid(row=i, column=j)
                fila.append(casilla)
            self.tablero_b.append(fila)

        # Inicializar piezas en el tablero A
        self.inicializar_piezas()

    def inicializar_piezas(self):
        piezas_blancas = ["\u2656", "\u2658", "\u2657", "\u2655", "\u2654", "\u2657", "\u2658", "\u2656"]
        piezas_negras = ["\u265C", "\u265E", "\u265D", "\u265B", "\u265A", "\u265D", "\u265E", "\u265C"]

        # Piezas negras
        for i in range(8):
            self.tablero_a[0][i].configure(text=piezas_negras[i], text_color="black")
            self.ocupacion_a[0][i] = piezas_negras[i]
            self.tablero_a[1][i].configure(text="\u265F", text_color="black")
            self.ocupacion_a[1][i] = "\u265F"

        # Piezas blancas
        for i in range(8):
            self.tablero_a[6][i].configure(text="\u2659", text_color="blue")
            self.ocupacion_a[6][i] = "\u2659"
            self.tablero_a[7][i].configure(text=piezas_blancas[i], text_color="blue")
            self.ocupacion_a[7][i] = piezas_blancas[i]
            
            


    def seleccionar_casilla(self, x, y, tablero):
        if self.pieza_seleccionada is None:
            self.intentar_seleccionar_pieza(x, y, tablero)
        else:
            self.mover_pieza(x, y, tablero)

    def intentar_seleccionar_pieza(self, x, y, tablero):
        casilla = self.obtener_casilla(x, y, tablero)
        if casilla.cget("text") != "":  # Hay una pieza en la casilla
            self.pieza_seleccionada = (x, y, tablero)
            casilla.configure(fg_color="yellow")
            self.mostrar_movimientos_legales(x, y, tablero)
            
            

    def mover_pieza(self, x, y, tablero):
        if self.pieza_seleccionada is not None:
            x_origen, y_origen, tablero_origen = self.pieza_seleccionada
            casilla_origen = self.obtener_casilla(x_origen, y_origen, tablero_origen)
            pieza = casilla_origen.cget("text")
            color_pieza = casilla_origen.cget("text_color")

            if tablero != tablero_origen and self.movimiento_valido(x, y, x_origen, y_origen, pieza, tablero):
                # Actualizar visualmente
                casilla_origen.configure(text="", fg_color=("beige" if (x_origen + y_origen) % 2 == 0 else "brown"))
                casilla_destino = self.obtener_casilla(x, y, tablero)
                casilla_destino.configure(text=pieza, text_color=color_pieza)

                # Actualizar ocupación
                self.actualizar_ocupacion(x, y, x_origen, y_origen, pieza, tablero, tablero_origen)

                # Limpiar selección y movimientos legales
                self.pieza_seleccionada = None
                self.limpiar_movimientos_legales(tablero_origen)
                self.limpiar_movimientos_legales(tablero)
            else:
                self.limpiar_movimientos_legales(tablero_origen)
                self.limpiar_movimientos_legales(tablero)
                messagebox.showinfo("Movimiento inválido", "Movimiento no permitido.")
                self.limpiar_seleccion()
                
    def actualizar_ocupacion(self, x, y, x_origen, y_origen, pieza, tablero, tablero_origen):
        # Actualizar ocupación lógica
        if tablero_origen == 'A':
            self.ocupacion_a[x_origen][y_origen] = None
        else:
            self.ocupacion_b[x_origen][y_origen] = None

        if tablero == 'A':
            self.ocupacion_a[x][y] = pieza
        else:
            self.ocupacion_b[x][y] = pieza
                
                

    def movimiento_valido(self, x, y, x_origen, y_origen, pieza, tablero):
        dx, dy = abs(x - x_origen), abs(y - y_origen)
        direccion = -1 if pieza == "\u2659" else 1  # Blancos avanzan positivo, negros negativo
        
         # Verificar si la casilla destino está ocupada en el tablero correspondiente
        ocupacion_destino = self.ocupacion_a if tablero == 'A' else self.ocupacion_b
        if ocupacion_destino[x][y] is not None:
            return False

        if pieza in ["\u2659", "\u265F"]:  # Peón
            # Avance simple
            if dy == 0 and dx == 1:
                return x == x_origen + direccion
            # Avance doble desde posición inicial
            if dy == 0 and dx == 2:
                inicio = 6 if pieza == "\u2659" else 1
                return x_origen == inicio and x == x_origen + 2 * direccion
            # Captura en diagonal
            if dy == 1 and dx == 1:
                destino = self.obtener_casilla(x, y, tablero)
                return destino.cget("text") != "" and self.es_ficha_opuesta(pieza, destino.cget("text"))
            return False  
        
        
        
        elif pieza in ["\u2658", "\u265E"]:  # Caballo
            return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
        elif pieza in ["\u2656", "\u265C"]:  # Torre
            return (dx == 0 and dy > 0) or (dy == 0 and dx > 0)
        elif pieza in ["\u2657", "\u265D"]:  # Alfil
            return dx == dy
        elif pieza in ["\u2655", "\u265B"]:  # Reina
            return (dx == dy) or (dx == 0 or dy == 0)
        elif pieza in ["\u2654", "\u265A"]:  # Rey
            return dx <= 1 and dy <= 1
        return super().movimiento_valido(x, y, x_origen, y_origen, pieza, tablero)
    
        

    def mostrar_movimientos_legales(self, x, y, tablero):
        pieza = self.obtener_casilla(x, y, tablero).cget("text")
        tablero_opuesto = 'B' if tablero == 'A' else 'A'
        for i in range(8):
            for j in range(8):
                if self.movimiento_valido(i, j, x, y, pieza, tablero_opuesto):
                    casilla = self.obtener_casilla(i, j, tablero_opuesto)
                    casilla.configure(fg_color="green")

    def obtener_casilla(self, x, y, tablero):
        if tablero == 'A':
            return self.tablero_a[x][y] 
        else:
            return self.tablero_b[x][y]

    def limpiar_movimientos_legales(self, tablero):
        tablero_actual = self.tablero_a if tablero == 'A' else self.tablero_b
        for i in range(8):
            for j in range(8):
                casilla = tablero_actual[i][j]
                casilla.configure(fg_color=("beige" if (i + j) % 2 == 0 else "brown"))

    def limpiar_seleccion(self):
        if self.pieza_seleccionada is not None:
            x, y, tablero = self.pieza_seleccionada
            casilla = self.obtener_casilla(x, y, tablero)
            casilla.configure(fg_color=("beige" if (x + y) % 2 == 0 else "brown"))
        self.pieza_seleccionada = None

# Inicializar la interfaz gráfica
root = ctk.CTk()
root.geometry("700x400")
root.title("Ajedrez de Alicia")
ajedrez = AjedrezAlicia(root)
root.mainloop()
