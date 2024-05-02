class Product:
    def __init__(self, id=0, descrip="Ninguno", preci=0, stock=0):
        # Método constructor para inicializar los atributos de la clase Product
        self.__id = id
        self.descrip = descrip
        self.preci = preci
        self.__stock = stock  # Atributo privado para almacenar la cantidad en stock

    @property
    def stock(self):
        # Getter para obtener el valor del atributo privado __stock
        return self.__stock

    @stock.setter
    def stock(self, value):
        # Setter para asignar un nuevo valor a __stock
        if value >= 0:
            self.__stock = value
        else:
            raise ValueError("El stock debe ser un valor positivo o cero.")

    def __repr__(self):
        # Método especial para representar la clase Product como una cadena
        return f'Producto: {self.__id} {self.descrip} {self.preci} {self.stock}'

    def __str__(self):
        # Método especial para representar la clase Product como una cadena
        return f'Producto: {self.__id} {self.descrip} {self.preci} {self.stock}'

    def getJson(self):
        # Método para convertir la instancia de Product a un diccionario (formato JSON)
        return {"id": self.__id, "descripcion": self.descrip, "precio": self.preci, "stock": self.stock}