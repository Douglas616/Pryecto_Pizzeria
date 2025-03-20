class Nodo:
    def __init__(self, cliente, cantidad, ingredientes):
        self.cliente = cliente
        self.cantidad = cantidad
        self.ingredientes = ingredientes
        self.tiempo_preparacion = self.calcular_tiempo()
        self.siguiente = None 