# Definición de la clase Usuario
class Usuario:
    def __init__(self, nombre, usuario_id, contraseña):
        self.nombre = nombre
        self.usuario_id = usuario_id
        self.__contraseña = contraseña

    def validar_contraseña(self, contraseña):
        return self.__contraseña == contraseña


# Definición de la clase base CuentaBancaria
class CuentaBancaria:
    def __init__(self, usuario, numero_cuenta):
        self.usuario = usuario
        self.numero_cuenta = numero_cuenta
        self.saldo = 0

    def depositar(self, cantidad):
        if cantidad > 0:
            self.saldo += cantidad
            print(f"Depósito exitoso. Nuevo saldo: {self.saldo}")
        else:
            print("La cantidad debe ser positiva.")

    def retirar(self, cantidad):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    def transferir(self, cuenta_destino, cantidad):
        if 0 < cantidad <= self.saldo:
            self.saldo -= cantidad
            cuenta_destino.saldo += cantidad
            print(f"Transferencia exitosa. Nuevo saldo: {self.saldo}")
        else:
            print("Fondos insuficientes o cantidad inválida.")

    def mostrar_saldo(self):
        print(f"Saldo actual: {self.saldo}")


# Definición de la clase CuentaAhorros
class CuentaAhorros(CuentaBancaria):
    def retirar(self, cantidad):
        if 0 < cantidad <= self.saldo:
            self.saldo -= cantidad
            print(f"Retiro exitoso. Nuevo saldo: {self.saldo}")
        else:
            print("Fondos insuficientes o cantidad inválida.")


# Definición de la clase CuentaCorriente
class CuentaCorriente(CuentaBancaria):
    def __init__(self, usuario, numero_cuenta, sobregiro_maximo):
        super().__init__(usuario, numero_cuenta)
        self.sobregiro_maximo = sobregiro_maximo

    def retirar(self, cantidad):
        if 0 < cantidad <= self.saldo + self.sobregiro_maximo:
            self.saldo -= cantidad
            print(f"Retiro exitoso. Nuevo saldo: {self.saldo}")
        else:
            print("Fondos insuficientes incluso con sobregiro.")


# Definición de la clase SistemaBanco
class SistemaBanco:
    def __init__(self):
        self.usuarios = []
        self.cuentas = []

    def registrar_usuario(self, nombre, usuario_id, contraseña, tipo_cuenta, sobregiro_maximo=0):
        nuevo_usuario = Usuario(nombre, usuario_id, contraseña)
        if tipo_cuenta == "ahorros":
            nueva_cuenta = CuentaAhorros(nuevo_usuario, len(self.cuentas) + 1)
        elif tipo_cuenta == "corriente":
            nueva_cuenta = CuentaCorriente(nuevo_usuario, len(self.cuentas) + 1, sobregiro_maximo)
        else:
            raise ValueError("Tipo de cuenta no válido.")
        self.usuarios.append(nuevo_usuario)
        self.cuentas.append(nueva_cuenta)
        print(f"Usuario {nombre} registrado exitosamente. Número de cuenta: {nueva_cuenta.numero_cuenta}")

    def iniciar_sesion(self, usuario_id, contraseña):
        for usuario in self.usuarios:
            if usuario.usuario_id == usuario_id and usuario.validar_contraseña(contraseña):
                print(f"Bienvenido {usuario.nombre}")
                return usuario
        print("ID de usuario o contraseña incorrecta.")
        return None

    def encontrar_cuenta(self, numero_cuenta):
        for cuenta in self.cuentas:
            if cuenta.numero_cuenta == numero_cuenta:
                return cuenta
        print("Cuenta no encontrada.")
        return None


# Ejemplo de uso
if __name__ == "__main__":
    banco = SistemaBanco()
    
    # Registro de usuarios
    banco.registrar_usuario("Alice", "alice123", "password1", "ahorros")
    banco.registrar_usuario("Bob", "bob456", "password2", "corriente", sobregiro_maximo=500)
    
    # Inicio de sesión
    usuario1 = banco.iniciar_sesion("alice123", "password1")
    usuario2 = banco.iniciar_sesion("bob456", "password2")
    
    # Operaciones bancarias
    if usuario1:
        cuenta1 = banco.encontrar_cuenta(1)
        cuenta1.depositar(500)
        cuenta1.mostrar_saldo()
        cuenta1.retirar(100)
        cuenta1.mostrar_saldo()
    
    if usuario2:
        cuenta2 = banco.encontrar_cuenta(2)
        cuenta1.transferir(cuenta2, 200)
        cuenta1.mostrar_saldo()
        cuenta2.mostrar_saldo()
        cuenta2.retirar(600)  # Incluye sobregiro
        cuenta2.mostrar_saldo()
