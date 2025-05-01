import os
import xml.etree.ElementTree as ET
import heapq
import subprocess
import tkinter as tk
from tkinter import filedialog

class Terreno:
    def __init__(self, nombre, matriz, inicio, fin):
        self.nombre = nombre
        self.matriz = matriz
        self.inicio = inicio
        self.fin = fin
        self.filas = len(matriz)
        self.columnas = len(matriz[0])

    def encontrar_ruta_optima(self):
        dx = [0, 0, 1, -1]
        dy = [1, -1, 0, 0]
        inicio_x, inicio_y = self.inicio
        fin_x, fin_y = self.fin

        heap = [(self.matriz[inicio_x][inicio_y], inicio_x, inicio_y)]
        distancias = {(i, j): float('inf') for i in range(self.filas) for j in range(self.columnas)}
        distancias[(inicio_x, inicio_y)] = self.matriz[inicio_x][inicio_y]
        padre = {}

        while heap:
            costo, x, y = heapq.heappop(heap)
            if (x, y) == (fin_x, fin_y):
                break
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                    nuevo_costo = costo + self.matriz[nx][ny]
                    if nuevo_costo < distancias[(nx, ny)]:
                        distancias[(nx, ny)] = nuevo_costo
                        heapq.heappush(heap, (nuevo_costo, nx, ny))
                        padre[(nx, ny)] = (x, y)

        camino = []
        actual = (fin_x, fin_y)
        while actual in padre:
            camino.append(actual)
            actual = padre[actual]
        camino.append((inicio_x, inicio_y))
        camino.reverse()
        return camino

def generar_dot_matriz_con_camino(terreno, camino):
    n = terreno.filas
    m = terreno.columnas

    dot = []
    dot.append("graph G {")
    dot.append("    node [shape=box width=0.5];")
    dot.append("    splines=false;")
    dot.append("    nodesep=0.5;")
    dot.append("    ranksep=0.5;")

    # Crear nodos con colores específicos
    for i in range(n):
        fila_dot = []
        for j in range(m):
            valor = terreno.matriz[i][j]
            pos = f'"{i+1},{j+1}"'
            if (i, j) == terreno.inicio:
                estilo = 'style=filled, fillcolor=green'
            elif (i, j) == terreno.fin:
                estilo = 'style=filled, fillcolor=red'
            elif (i, j) in camino:
                estilo = 'style=filled, fillcolor=lightblue'
            else:
                estilo = ''
            nodo = f'{pos} [label="{valor}" {"," + estilo if estilo else ""}]'
            fila_dot.append(pos)
            dot.append(f'    {nodo};')
        dot.append("    { rank=same; " + "; ".join(fila_dot) + " }")

    # Conexiones horizontales
    for i in range(1, n + 1):
        for j in range(1, m):
            dot.append(f'    "{i},{j}" -- "{i},{j+1}";')

    # Conexiones verticales
    for i in range(1, n):
        for j in range(1, m + 1):
            dot.append(f'    "{i},{j}" -- "{i+1},{j}";')

    # Dibujar la ruta óptima como una línea resaltada
    for k in range(len(camino) - 1):
        i1, j1 = camino[k]
        i2, j2 = camino[k + 1]
        dot.append(f'    "{i1+1},{j1+1}" -- "{i2+1},{j2+1}" [color=blue, penwidth=2.5];')

    dot.append("}")

    archivo_dot = f"ruta_optima_{terreno.nombre}.dot"
    archivo_pdf = f"ruta_optima_{terreno.nombre}.pdf"

    with open(archivo_dot, "w") as f:
        f.write("\n".join(dot))

    print(f"Archivo DOT generado: {archivo_dot}")

    try:
        subprocess.run(["dot", "-Tpdf", archivo_dot, "-o", archivo_pdf], check=True)
        print(f"PDF generado: {archivo_pdf}")
        if os.name == 'nt':
            os.startfile(archivo_pdf)
        elif os.name == 'posix':
            subprocess.run(["xdg-open", archivo_pdf])
    except FileNotFoundError:
        print("Graphviz no está instalado o no se encontró el comando 'dot'.")

class GestorTerrenos:
    def __init__(self):
        self.terrenos = []

    def cargar_xml(self, archivo):
        tree = ET.parse(archivo)
        root = tree.getroot()
        for terreno in root.findall('terreno'):
            nombre = terreno.get('nombre')
            inicio = (int(terreno.find('posicioninicio/x').text) - 1, int(terreno.find('posicioninicio/y').text) - 1)
            fin = (int(terreno.find('posicionfin/x').text) - 1, int(terreno.find('posicionfin/y').text) - 1)
            matriz = {}
            for posicion in terreno.findall('posicion'):
                x, y = int(posicion.get('x')) - 1, int(posicion.get('y')) - 1
                valor = int(posicion.text)
                matriz[(x, y)] = valor
            filas = max(x for x, y in matriz.keys()) + 1
            columnas = max(y for x, y in matriz.keys()) + 1
            matriz_ordenada = [[matriz.get((i, j), 0) for j in range(columnas)] for i in range(filas)]
            self.terrenos.append(Terreno(nombre, matriz_ordenada, inicio, fin))

    def mostrar_terrenos(self):
        for i, terreno in enumerate(self.terrenos):
            print(f'{i+1}. {terreno.nombre}')

    def obtener_terreno(self, indice):
        return self.terrenos[indice]

def menu():
    gestor = GestorTerrenos()
    while True:
        print("\n--- Menú Principal del Quetzal 🤖---")
        print("1. Cargar archivo XML")
        print("2. Mostrar terrenos disponibles")
        print("3. Encontrar y graficar ruta óptima")
        print("4. Generar archivo salida xml")
        print("5. Mapa del Camino")
        print("6. Salir de menu")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            root = tk.Tk()
            root.withdraw()
            archivo = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
            if archivo:
                gestor.cargar_xml(archivo)
                print("Archivo cargado con éxito.")
            else:
                print("No se seleccionó ningún archivo.")
        elif opcion == "2":
            gestor.mostrar_terrenos()
        elif opcion == "3":
            gestor.mostrar_terrenos()
            indice = int(input("Seleccione el número de terreno: ")) - 1
            terreno = gestor.obtener_terreno(indice)
            camino = terreno.encontrar_ruta_optima()
            generar_dot_matriz_con_camino(terreno, camino)
            print("Ruta óptima generada y graficada en PDF.")
        elif opcion == "4":
           
         
            print("Ruta óptima generada y graficada como tabla.")
        elif opcion == "5":
            gestor.mostrar_terrenos()
            indice = int(input("Seleccione el número de terreno: ")) - 1
            terreno = gestor.obtener_terreno(indice)
            camino = terreno.encontrar_ruta_optima()
            matriz_visual = [['o' for _ in range(terreno.columnas)] for _ in range(terreno.filas)]
            for i, j in camino:
                matriz_visual[i][j] = '1'
            print("\nMapa del Camino (1 indica el recorrido):")
            for fila in matriz_visual:
                print(fila)
        elif opcion == "6":
            print("Saliendo.......")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
