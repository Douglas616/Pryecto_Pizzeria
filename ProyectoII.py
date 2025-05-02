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
        return camino, distancias[(fin_x, fin_y)]

def generar_dot_matriz_con_camino(terreno, camino):
    n = terreno.filas
    m = terreno.columnas

    dot = []
    dot.append("graph G {")
    dot.append("     node [shape=ellipse, width=1.5, height=0.7, fixedsize=true, style=filled, fillcolor=orange];")
    dot.append("     splines=false;")
    dot.append("     nodesep=0.5;")
    dot.append("     ranksep=0.5;")

    for i in range(n):
        fila_dot = []
        for j in range(m):
            valor = terreno.matriz[i][j]
            pos = f'"{i+1},{j+1}"'
            if (i, j) == terreno.inicio:
                estilo = 'style=filled, fillcolor=darkolivegreen2'
            elif (i, j) == terreno.fin:
                estilo = 'style=filled, fillcolor=crimson'
            elif (i, j) in camino:
                estilo = 'style=filled, fillcolor=cornflowerblue'
            else:
                estilo = ''
            nodo = f'{pos} [label="{valor}" {"," + estilo if estilo else ""}]'
            fila_dot.append(pos)
            dot.append(f'     {nodo};')
        dot.append("     { rank=same; " + "; ".join(fila_dot) + " }")

    for i in range(1, n + 1):
        for j in range(1, m):
            dot.append(f'     "{i},{j}" -- "{i},{j+1}";')

    for i in range(1, n):
        for j in range(1, m + 1):
            dot.append(f'     "{i},{j}" -- "{i+1},{j}";')

    for k in range(len(camino) - 1):
        i1, j1 = camino[k]
        i2, j2 = camino[k + 1]
        dot.append(f'     "{i1+1},{j1+1}" -- "{i2+1},{j2+1}" [color=blue, penwidth=2.5];')

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

    print(f"\nCoordenada inicial: ({terreno.inicio[0]+1},{terreno.inicio[1]+1})")
    print(f"Coordenada final: ({terreno.fin[0]+1},{terreno.fin[1]+1})")
    combustible_total = sum(terreno.matriz[x][y] for x, y in camino)
    print(f"Combustible necesario: {combustible_total} unidades")


class GestorTerrenos:
    def __init__(self):
        self.terrenos = []
        self.ruta_guardado_xml = "./salida_xml/" # Ruta por defecto para guardar los XML
        os.makedirs(self.ruta_guardado_xml, exist_ok=True)

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

       
    def generar_archivo_salida_xml(self, indice_terreno, nombre_archivo, ruta_optima, combustible_total):
        if 0 <= indice_terreno < len(self.terrenos):
            terreno = self.terrenos[indice_terreno]
            ruta_archivo = os.path.join(self.ruta_guardado_xml, f"{nombre_archivo}.xml")

            raiz = ET.Element("terreno")
            raiz.set("nombre", terreno.nombre)

            pos_ini = ET.SubElement(raiz, "posicioninicio")
            ET.SubElement(pos_ini, "x").text = str(terreno.inicio[0] + 1)
            ET.SubElement(pos_ini, "y").text = str(terreno.inicio[1] + 1)

            pos_fin = ET.SubElement(raiz, "posicionfin")
            ET.SubElement(pos_fin, "x").text = str(terreno.fin[0] + 1)
            ET.SubElement(pos_fin, "y").text = str(terreno.fin[1] + 1)

            combustible = ET.SubElement(raiz, "combustible")
            combustible.text = str(combustible_total)

            for x, y in ruta_optima:
                posicion = ET.SubElement(raiz, "posicion")
                posicion.set("x", str(x + 1))
                posicion.set("y", str(y + 1))
                posicion.text = str(terreno.matriz[x][y])

            arbol = ET.ElementTree(raiz)
            ET.indent(arbol, space="  ", level=0)

            try:
                arbol.write(ruta_archivo, encoding="UTF-8", xml_declaration=True)
                print(f"Archivo XML de salida generado exitosamente en: {ruta_archivo}")

                if os.name == 'nt':
                    try:
                        subprocess.run(["notepad.exe", ruta_archivo], check=True)
                    except FileNotFoundError:
                        print("No se encontró 'notepad.exe'.")
                elif os.name == 'posix':
                    try:
                        subprocess.run(["xdg-open", ruta_archivo], check=True)
                    except FileNotFoundError:
                        print("No se encontró un visor de texto predeterminado.")
            except Exception as e:
                print(f"Error al escribir el archivo XML: {e}")
        else:
            print("Índice de terreno no válido.")

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
            try:
                indice = int(input("Seleccione el número de terreno: ")) - 1
                terreno = gestor.obtener_terreno(indice)
                camino, combustible = terreno.encontrar_ruta_optima()
                generar_dot_matriz_con_camino(terreno, camino)
                print("Ruta óptima generada y graficada en PDF.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
            except IndexError:
                print("Número de terreno no válido.")
        elif opcion == "4":
            gestor.mostrar_terrenos()
            try:
                indice_terreno = int(input("Seleccione el número de terreno para generar el archivo XML: ")) - 1
                if 0 <= indice_terreno < len(gestor.terrenos):
                    nombre_archivo = input("Ingrese el nombre para el archivo XML de salida (sin extensión): ")
                    terreno = gestor.obtener_terreno(indice_terreno)
                    camino, combustible = terreno.encontrar_ruta_optima()
                    gestor.generar_archivo_salida_xml(indice_terreno, nombre_archivo, camino, combustible)
                else:
                    print("Número de terreno no válido.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
        elif opcion == "5":
            gestor.mostrar_terrenos()
            try:
                indice = int(input("Seleccione el número de terreno: ")) - 1
                terreno = gestor.obtener_terreno(indice)
                camino, _ = terreno.encontrar_ruta_optima()
                matriz_visual = [['o' for _ in range(terreno.columnas)] for _ in range(terreno.filas)]
                for i, j in camino:
                    matriz_visual[i][j] = '1'
                print("\nMapa del Camino (1 indica el recorrido):")
                for fila in matriz_visual:
                    print(fila)
            except ValueError:
                print("Por favor, ingrese un número válido.")
            except IndexError:
                print("Número de terreno no válido.")
        elif opcion == "6":
            print("Saliendo.......")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()