
class Nodo:
    def __init__(self, cliente, cantidad, ingredientes):
        self.cliente = cliente
        self.cantidad = cantidad
        self.ingredientes = ingredientes
        self.tiempo_preparacion = self.calcular_tiempo()
        self.siguiente = None  

    def calcular_tiempo(self):
        tiempos = {"Pepperoni": 3, "Salchicha": 4, "Carne": 10, "Queso": 5, "Piña": 2}
        return sum(tiempos[ing] for ing in self.ingredientes) * self.cantidad


class Cola:
    def __init__(self):
        self.frente = None  
        self.final = None   

    def encolar(self, cliente, cantidad, ingredientes):
        nuevo_nodo = Nodo(cliente, cantidad, ingredientes)
        if not self.frente:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        print(f"\n Orden agregada: {cliente} - {cantidad} pizza(s) ({', '.join(ingredientes)})")

    def desencolar(self):
        if not self.frente:
            print("\n⚠ No hay órdenes en la cola.")
            return
        orden = self.frente
        self.frente = self.frente.siguiente
        print(f"\n Orden despachada: {orden.cliente} - Tiempo total en cola: {orden.tiempo_preparacion} min")

    def mostrar_cola(self):
        if not self.frente:
            print("\n La cola está vacía.")
            return
        actual = self.frente
        print("\n Órdenes en espera:")
        while actual:
            print(f"🛎 Cliente: {actual.cliente} | Pizzas: {actual.cantidad} | Ingredientes: {', '.join(actual.ingredientes)}")
            actual = actual.siguiente


def menu():
    cola = Cola()
    while True:
        print("\n Bienvendios a Douglas´ Pizza")
        print(" ")
        print("\n MENÚ PRINCIPAL ")
        print("1. Agregar orden")
        print("2. Despachar orden")
        print("3. Mostrar cola")
        print("4. Datos del desarrollador")
        print("5. Ingredientes disponibles")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cliente = input("\n👤 Nombre del cliente: ")
            cantidad = int(input(" Cantidad de pizzas: "))
            ingredientes = input(" Ingredientes (separados por comas): ").split(", ")
            cola.encolar(cliente, cantidad, ingredientes)

        elif opcion == "2":
            cola.desencolar()

        elif opcion == "3":
            cola.mostrar_cola()

        elif opcion == "4":
            print("\n👨‍💻 Desarrollado por: Douglas´ Pizza")

        elif opcion == "5":
            print("\n Ingredientes:")
            print("Pepperoni")
            print("Salchicha")
            print("arne")
            print("Queso")
            print("Piña")

        elif opcion == "6":
            print("\n Saliendo del programa...")
            break

        else:
            print("\n Opción inválida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
