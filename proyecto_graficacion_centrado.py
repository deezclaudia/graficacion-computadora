
import tkinter as tk
from tkinter import ttk, colorchooser


class GraficacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Final - Graficación por Computadora")
        self.root.geometry("1050x650")

        self.canvas_width = 800
        self.canvas_height = 600

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack(side="left", padx=10, pady=10)


        self.origin_x = self.canvas_width // 2
        self.origin_y = self.canvas_height // 2


        frame = tk.Frame(root)
        frame.pack(side="right", fill="y", padx=10, pady=10)

        tk.Label(frame, text="Menú de Opciones", font=("Arial", 16, "bold")).pack(pady=5)

        ttk.Button(frame, text="Línea DDA", command=self.menu_linea_dda).pack(fill="x", pady=3)
        ttk.Button(frame, text="Línea Bresenham", command=self.menu_linea_bresenham).pack(fill="x", pady=3)
        ttk.Button(frame, text="Círculo Punto Medio", command=self.menu_circulo_pm).pack(fill="x", pady=3)

        # Caja de coordenadas
        tk.Label(frame, text="Coordenadas generadas:", font=("Arial", 12, "bold")).pack(pady=5)
        self.text_coords = tk.Text(frame, width=30, height=25)
        self.text_coords.pack()


    def to_screen(self, x, y):
        screen_x = self.origin_x + x
        screen_y = self.origin_y - y
        return screen_x, screen_y


    def menu_linea_dda(self):
        self.ventana_datos("Línea DDA", self.dibujar_linea_dda)

    def menu_linea_bresenham(self):
        self.ventana_datos("Línea Bresenham", self.dibujar_linea_bresenham)

    def menu_circulo_pm(self):
        self.ventana_circulo("Círculo Punto Medio", self.dibujar_circulo_pm)



    def ventana_datos(self, titulo, funcion):
        win = tk.Toplevel(self.root)
        win.title(titulo)

        campos = ["X inicial", "Y inicial", "X final", "Y final"]
        entradas = {}

        for c in campos:
            tk.Label(win, text=c).pack()
            e = tk.Entry(win)
            e.pack()
            entradas[c] = e

        def seleccionar_color():
            color = colorchooser.askcolor()[1]
            entradas["color"] = color

        ttk.Button(win, text="Elegir color", command=seleccionar_color).pack(pady=5)

        def ejecutar():
            self.canvas.delete("all")
            self.text_coords.delete("1.0", tk.END)
            try:
                xi = int(entradas["X inicial"].get())
                yi = int(entradas["Y inicial"].get())
                xf = int(entradas["X final"].get())
                yf = int(entradas["Y final"].get())
                color = entradas.get("color", "white")
                funcion(xi, yi, xf, yf, color)
            except:
                print("Error en los datos")

        ttk.Button(win, text="Dibujar", command=ejecutar).pack(pady=10)

    def ventana_circulo(self, titulo, funcion):
        win = tk.Toplevel(self.root)
        win.title(titulo)

        campos = ["Radio", "X centro", "Y centro"]
        entradas = {}

        for c in campos:
            tk.Label(win, text=c).pack()
            e = tk.Entry(win)
            e.pack()
            entradas[c] = e

        def seleccionar_color():
            color = colorchooser.askcolor()[1]
            entradas["color"] = color

        ttk.Button(win, text="Elegir color", command=seleccionar_color).pack(pady=5)

        def ejecutar():
            self.canvas.delete("all")
            self.text_coords.delete("1.0", tk.END)
            try:
                r = int(entradas["Radio"].get())
                xc = int(entradas["X centro"].get())
                yc = int(entradas["Y centro"].get())
                color = entradas.get("color", "white")
                funcion(r, xc, yc, color)
            except:
                print("Error en los datos")

        ttk.Button(win, text="Dibujar", command=ejecutar).pack(pady=10)



    def dibujar_linea_dda(self, x1, y1, x2, y2, color):
        dx = x2 - x1
        dy = y2 - y1
        pasos = max(abs(dx), abs(dy))
        x_inc = dx / pasos
        y_inc = dy / pasos

        x = x1
        y = y1

        for _ in range(pasos + 1):
            sx, sy = self.to_screen(int(x), int(y))
            self.canvas.create_rectangle(sx, sy, sx+1, sy+1, outline=color)
            self.text_coords.insert(tk.END, f"{int(x)}  {int(y)}\n")
            x += x_inc
            y += y_inc

    def dibujar_linea_bresenham(self, x1, y1, x2, y2, color):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        x, y = x1, y1

        while True:
            sx2, sy2 = self.to_screen(x, y)
            self.canvas.create_rectangle(sx2, sy2, sx2+1, sy2+1, outline=color)
            self.text_coords.insert(tk.END, f"{x}  {y}\n")

            if x == x2 and y == y2:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def dibujar_circulo_pm(self, r, xc, yc, color):
        x = 0
        y = r
        p = 1 - r

        while x <= y:
            puntos = [
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ]

            for px, py in puntos:
                sx, sy = self.to_screen(px, py)
                self.canvas.create_rectangle(sx, sy, sx+1, sy+1, outline=color)
                self.text_coords.insert(tk.END, f"{px}  {py}\n")

            if p < 0:
                p += 2 * x + 3
            else:
                p += 2 * (x - y) + 5
                y -= 1
            x += 1


if __name__ == "__main__":
    root = tk.Tk()
    app = GraficacionApp(root)
    root.mainloop()
