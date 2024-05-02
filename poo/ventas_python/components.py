from utilities import borrarPantalla, gotoxy
import time
import re

class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   

class Valida:
    def solo_numeros(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)            
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor

    def validar_nombres(self, nombres):
        # Patrón regex para validar nombres (solo letras, espacios y apóstrofes)
        patron = r"^[A-Za-z\s'-]+$"
        # Verifica si los nombres coinciden con el patrón válido
        if re.match(patron, nombres):
            return True
        return False

    # Función para validar los apellidos
    def validar_apellidos(self, apellidos):
        # Patrón regex para validar apellidos (solo letras, espacios y apóstrofes)
        patron = r"^[A-Za-z\s'-]+$"
        # Verifica si los apellidos coinciden con el patrón válido
        if re.match(patron, apellidos):
            return True
        return False

    def solo_decimales(self,mensaje,mensajeError):
        while True:
            valor = str(input("          ------>   | {} ".format(mensaje)))
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except:
                print("          ------><  | {} ".format(mensajeError))
        return valor
    
    def validar_cedula(self,dni):
        # Verifica si la longitud de la cédula es de 10 dígitos (DNI) o 13 dígitos (RUC)
        if len(dni) == 10 or len(dni) == 13:
            # Verifica que la cédula contenga solo números
            if dni.isdigit():
                return True
        return False
    
class otra:
    pass    

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)