import graphviz
from graphviz import Digraph

class Nodo:
    def __init__(self, cliente, cantidad, ingredientes):
        self.cliente = cliente
        self.cantidad = cantidad
        self.ingredientes = ingredientes
        self.tiempo_preparacion = self.calcular_tiempo()
        self.siguiente = None

    def calcular_tiempo(self):
        tiempos = {"Pepperoni": 3, "Salchicha": 4, "Carne": 10, "Queso": 5, "Piña": 2}
        return sum(tiempos.get(ing, 5) for ing in self.ingredientes) * self.cantidad


class Cola:
    def __init__(self):
        self.frente = None
        self.final = None

    def Encolar(self, cliente, cantidad, ingredientes):
        nuevo_nodo = Nodo(cliente, cantidad, ingredientes)
        if not self.frente:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        print(f"\n\033[92m✅ Orden agregada: {cliente} - {cantidad} pizza(s) ({', '.join(ingredientes)})\033[0m")

    def Desencolar(self):
        if not self.frente:
            print("\n\033[93m⚠ No hay órdenes en la cola.\033[0m")
            return
        orden = self.frente
        self.frente = self.frente.siguiente
        print(f"\n\033[94m🚚 Orden despachada: {orden.cliente} - Tiempo total en cola: {orden.tiempo_preparacion} min\033[0m")

    def mostrar_cola(self):
        if not self.frente:
            print("\n\033[91m📭 La cola está vacía.\033[0m")
            return
        actual = self.frente
        print("\n\033[96m📋 Órdenes en espera:\033[0m")
        while actual:
            print(f"🍕 Cliente: {actual.cliente} | Pizzas: {actual.cantidad} | Ingredientes: {', '.join(actual.ingredientes)}")
            actual = actual.siguiente

    def generar_grafico_cola(self):
        dot = Digraph(comment='Cola de Pedidos', graph_attr={'rankdir': 'LR'})
        actual = self.frente
        contador = 0

        while actual:
            label = f"Cliente: {actual.cliente}\nPizzas: {actual.cantidad}\nIngredientes: {', '.join(actual.ingredientes)}"
            dot.node(f'nodo{contador}', label=label, shape='box', style='filled', fillcolor='orange')
            if contador > 0:
                dot.edge(f'nodo{contador - 1}', f'nodo{contador}')
            actual = actual.siguiente
            contador += 1

        dot.render('cola_pedidos.gv', view=True)


def menu():
    cola = Cola()
    ingredientes_disponibles = ["Pepperoni", "Salchicha", "Carne", "Queso", "Piña"]

    ingredientes = ["Pepperoni", "Salchicha", "Carne", "Queso", "Piña"]
    print("\n\033[33m🍕 Bienvenidos a Pizza's Douglas 🍕\033[0m")
    print("\n\033[92mIngredientes disponibles:\033[0m")
    for ing in ingredientes:
        print(f"- {ing}")

    while True:
        print("\n\033[38;5;214m__________________MENÚ PRINCIPAL__________________\033[0m")
        print("Seleccione una de las siguiente opciones del Menu: 🍴")
        print("1. Añadir orden")
        print("2. Despachar orden")
        print("3. Mostrar cola")
        print("4. Datos del desarrollador")
        print("5. Salir de Menu") 
        opcion = input("Ingrese un número para indicar una opción: ")

        if opcion == "1":
            print("Complete los siguientes campos")
            cliente = input("\n👤 Nombre del cliente: ")
            cantidad = int(input("Cantidad de pizzas: "))
            print("\n📜 Ingredientes disponibles:")
            for i, ing in enumerate(ingredientes_disponibles, 1):
                print(f"{i}. {ing}")
            
            seleccion = input("👉 Seleccione ingredientes (numeros separados por espacios): ").split()
            ingredientes = [ingredientes_disponibles[int(i) - 1] for i in seleccion if i.isdigit()]
            
            cola.Encolar(cliente, cantidad, ingredientes)

        elif opcion == "2":
            cola.Desencolar()

        elif opcion == "3":
            cola.mostrar_cola()
            cola.generar_grafico_cola()

        elif opcion == "4":
            print("\n\033[93m👨‍💻 Desarrollado por: Douglas Esaú Catú Otzoy 000140060 \033[0m")

        elif opcion == "5":
            print("\n\033[34m👋 Saliendo del Menu... Gracias por visitarnos!😊\033[0m")
            break

        else:
            print("\n\033[31m❌ Opción inválida, intenta de nuevo.\033[0m")


if __name__ == "__main__":
    menu()
