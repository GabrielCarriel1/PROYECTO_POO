import json
class JsonFile:
    def __init__(self, filename):
        self.filename = filename
        
    def save(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file)# dump:graba datos a un archivo json
      
    def read(self):
        try:
            with open(self.filename,'r') as file:
                data = json.load(file)# load:carga datos desde un archivo json
        except FileNotFoundError:
            data = []
        return data
     
    def find(self,atributo,buscado):
        try:
            with open(self.filename,'r') as file:
                datas = json.load(file)
                data = [item for item in datas if item[atributo] == buscado ]
        except FileNotFoundError:
            data = []
        return data
    def delete(self, atributo, valor):
        # Elimina elementos que coinciden con el atributo y valor especificados
        data = self.read()
        
        # Filtra los datos para eliminar los elementos que coinciden con el atributo y valor
        data_actualizada = [item for item in data if item[atributo] != valor]
        
        # Guarda los datos actualizados en el archivo JSON
        self.save(data_actualizada)
        
        # Retorna True si se eliminó algún elemento, False si no se eliminó ninguno
        return len(data) != len(data_actualizada)