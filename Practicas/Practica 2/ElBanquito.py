from colorama import Fore, Style, init
init(autoreset=True)


class Usuario:
    def __init__(self, nom_usuario, id_usuario, saldo_inicial):
        self.nom_usuario = nom_usuario
        self.id_usuario = id_usuario
        self.saldo = saldo_inicial
        self.cuentas = []

    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)


class Cuenta:
    def __init__(self, tipo, saldo_inicial):
        self.tipo = tipo
        self.saldo = saldo_inicial

    def Deposito(self, cantidad):
        self.saldo += cantidad
        print(f"Deposito exitoso. Nuevo saldo: {self.saldo}")

    def Retiro(self, cantidad):
        raise NotImplementedError("Este metodo debe ser implementado por las subclases")

    def mostrar_saldo(self):
        print(f"Saldo actual: {self.saldo}")


class CuentaAhorros(Cuenta):
    def __init__(self, saldo_inicial):
        super().__init__("Ahorros", saldo_inicial)

    def Retiro(self, cantidad):
        if cantidad > self.saldo:
            print(Fore.RED +"Saldo insuficiente.")
        else:
            self.saldo -= cantidad
            print(f"Retiro exitoso. Nuevo saldo: {self.saldo}")


class CuentaNormal(Cuenta):
    def __init__(self, saldo_inicial, max_sobregiro):
        super().__init__("Normal", saldo_inicial)
        self.max_sobregiro = max_sobregiro

    def Retiro(self, cantidad):
        if cantidad > self.saldo + self.max_sobregiro:
            print(Fore.RED +"Saldo insuficiente.")
        else:
            self.saldo -= cantidad
            print(f"Retiro exitoso. Nuevo saldo: {self.saldo}")


def crear_cuenta():
    nom_usuario = input("Ingrese el nombre del usuario: ")
    id_usuario = input("Ingrese el ID del usuario: ")
    saldo_inicial = float(input("Ingrese el saldo inicial de la nueva cuenta: "))
    tipo_cuenta = input("Ingrese el tipo de cuenta (ahorros/normal): ").lower()

    nuevo_usuario = Usuario(nom_usuario, id_usuario, saldo_inicial)

    if tipo_cuenta == "ahorros":
        nueva_cuenta = CuentaAhorros(saldo_inicial)
    elif tipo_cuenta == "normal":
        max_sobregiro = float(input("Ingrese el límite de sobregiro: "))
        nueva_cuenta = CuentaNormal(saldo_inicial, max_sobregiro)
    else:
        print(Fore.RED +"Tipo de cuenta no valido. Intentelo de nuevo.")
        return None, None

    return nuevo_usuario, nueva_cuenta


def Menu():
    print("Menú:")
    print("1- Dar de alta una cuenta")
    print("2- Transferir")
    print("3- Depositar")
    print("4- Retirar")
    print("5- Mostrar Cuenta")
    print("6- Salir")


def Deposito():
    id_usuario = input("Ingrese el ID de usuario: ")
    usuario_encontrado = False
    if not usuario_encontrado:
        print("No se encontro el usuario con el ID proporcionado.")
    else:
        monto = float(input("Ingrese el monto a Deposito: "))
    
    for usuario in usuarios:
        if usuario.id_usuario == id_usuario:
            usuario_encontrado = True
            usuario.saldo += monto
            print(Fore.GREEN+"Deposito realizado con exito.")
            break
  

def Transferencia():
    id_origen = input("Ingrese el ID de origen de la cuenta: ")
    id_destino = input("Ingrese el ID de destino de la cuenta: ")
    monto = float(input("Ingrese el monto a transferir: "))

    usuario_origen = None
    usuario_destino = None

    for usuario in usuarios:
        if usuario.id_usuario == id_origen:
            usuario_origen = usuario
        elif usuario.id_usuario == id_destino:
            usuario_destino = usuario

    if usuario_origen is None:
        print(Fore.RED +"El usuario de origen no existe.")
    elif usuario_destino is None:
        print(Fore.RED +"El usuario de destino no existe.")
    elif usuario_origen.saldo < monto:
        print(Fore.RED +"Saldo insuficiente para realizar la transferencia.")
    else:
        usuario_origen.saldo -= monto
        usuario_destino.saldo += monto
        print(Fore.GREEN +"Transferencia realizada con exito.")


def Mostrar_cuenta():
    id_usuario = input("Ingrese el ID de usuario: ")
    usuario_encontrado = False
    for usuario in usuarios:
        if usuario.id_usuario == id_usuario:
            usuario_encontrado = True
            print(Fore.GREEN + "==============================")
            print(Fore.YELLOW + f"Nombre de usuario: {usuario.nom_usuario}")
            print(Fore.YELLOW + f"ID de usuario: {usuario.id_usuario}")
            print(Fore.YELLOW + f"Saldo de la cuenta: {usuario.saldo}")
            for cuenta in usuario.cuentas:
                print(Fore.CYAN + f"Tipo de cuenta: {cuenta.tipo}")
                print(Fore.CYAN + f"Saldo: {cuenta.saldo}")
            print(Fore.GREEN + "==============================")
            break
    if not usuario_encontrado:
        print(Fore.RED + "No se encontró el usuario con el ID proporcionado.")


def Retiro():
    id_usuario = input("Ingrese el ID de usuario: ")
    monto = float(input("Ingrese el monto a Retiro: "))

    usuario_encontrado = False
    for usuario in usuarios:
        if usuario.id_usuario == id_usuario:
            usuario_encontrado = True
            if usuario.saldo < monto:
                print(Fore.RED +"Saldo insuficiente para realizar el retiro.")
            else:
                usuario.saldo -= monto
                print(Fore.GREEN +"Retiro realizado con exito.")
            break

    if not usuario_encontrado:
        print(Fore.RED +"No se encontro el usuario con el ID proporcionado.")


def Alta_cuenta():
    nuevo_usuario, nueva_cuenta = crear_cuenta()
    if nuevo_usuario and nueva_cuenta:
        usuarios.append(nuevo_usuario)
        nuevo_usuario.agregar_cuenta(nueva_cuenta)
        print(Fore.GREEN +"Cuenta creada exitosamente.")


usuarios = []

while True:
    
    Menu()
    
    opcion = input("Seleccione una opcion (1,2,3,4,5,6): ")

    if opcion == "1":
        Alta_cuenta()

    elif opcion == "2":
        Transferencia()

    elif opcion == "3":
        Deposito()

    elif opcion == "4":
        Retiro()

    elif opcion == "5":
        Mostrar_cuenta()

    elif opcion == "6":
        print("Gracias por utilizar nuestro sistema.")
        break

    else:
        print(Fore.RED +"Opcion no valida. Por favor, seleccione una opcion valida.")
