import graphviz
from graphviz import Digraph

class Nodo:
    def __init__(self, cliente, cantidad, ingredientes):
        self.cliente = cliente
        self.cantidad = cantidad
        self.ingredientes = ingredientes
        self.tiempo_preparacion = self.calcular_tiempo_de_entrega()
        self.siguiente = None

    def calcular_tiempo_de_entrega(self):
        duracion = {"Pepperoni": 3, "Salchicha": 4, "Carne": 10, "Queso": 5, "Piña": 2}
        return sum(duracion.get(ing, 5) for ing in self.ingredientes) * self.cantidad


class Cola: 
    def __init__(self): 
        self.frente_pedido = None 
        self.final_pedido = None 

    def Encolar(self, cliente, cantidad, ingredientes): #Agregar pedido 
        Nuevo = Nodo(cliente, cantidad, ingredientes)
        if not self.frente_pedido:
            self.frente_pedido = self.final_pedido = Nuevo
        else:
            self.final_pedido.siguiente = Nuevo
            self.final_pedido = Nuevo
        print(f"\n\033[92m✅ Orden agregada: {cliente} - {cantidad} pizza(s) ({', '.join(ingredientes)})\033[0m")

    def Desencolar(self): #Eliminar pedido
        if not self.frente_pedido:
            print("\n\033[93m⚠ No hay órdenes en la cola.\033[0m")
            return
        orden = self.frente_pedido
        self.frente_pedido = self.frente_pedido.siguiente
        print(f"\n\033[94m🚚 Orden despachada: {orden.cliente} - Tiempo total en cola: {orden.tiempo_preparacion} min\033[0m")

    def mostrar_cola(self): # Muesta los pedidos que aun estan pendientes
        if not self.frente_pedido:
            print("\n\033[91m📭 La cola está vacía.\033[0m")
            return
        actual = self.frente_pedido
        print("\n\033[96m📋 Órdenes en espera:\033[0m")
        while actual:
            print(f"🍕 Cliente: {actual.cliente} | Pizzas: {actual.cantidad} | Ingredientes: {', '.join(actual.ingredientes)}")
            actual = actual.siguiente

    def generar_grafico_cola(self):
        dot = Digraph(comment='Cola de Pedidos', graph_attr={'rankdir': 'LR'}) #TB = H
        pedido_actual = self.frente_pedido
        contador = 0

        while pedido_actual:
            label = f"Cliente: {pedido_actual.cliente}\nPizzas: {pedido_actual.cantidad}\nIngredientes: {', '.join(pedido_actual.ingredientes)}"
            dot.node(f'nodo{contador}', label=label, shape='box', style='filled', fillcolor='orange')
            if contador > 0:
                dot.edge(f'nodo{contador - 1}', f'nodo{contador}')
            pedido_actual = pedido_actual.siguiente
            contador += 1

        dot.render('grafico_cola_de_pedidos.gv', view=True)


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
        print("Seleccione una de las siguiente opciones del Menú: 🍴")
        print("1. Añadir orden")
        print("2. Despachar orden")
        print("3. Mostrar cola")
        print("4. Datos del diseñador de programas")
        print("5. Salir del Menu") 
        opcion = input("Ingrese un número para indicar su opción: ")

        if opcion == "1":
            print("Complete los siguientes campos")
            cliente = input("\n👤 Nombre del cliente: ")


            while True:
                try:
                    cantidad = int(input("🍕Cantidad de pizzas:"))
                    if cantidad > 0:
                        break
                    else:
                        
                        print("Ingresa un número mayor a 0")
                except ValueError:    
                        print("Opción inválida. Ingrese un número entero")
        
            
            print("\n📜 Ingredientes disponibles:")
            for i, ing in enumerate(ingredientes_disponibles, 1):
                print(f"{i}. {ing}")
            
            seleccion = input("👉 Seleccione ingredientes (números separados por espacios): ").split()
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
