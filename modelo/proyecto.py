import datetime
import pickle

class Usuarios:
    def __init__(self):
        self.registros_usuarios = {}

    def registrar_usuario(self):
        print("Registro de Usuario")
        nombre_usuario = input("Ingrese su nombre de usuario: ")
        if nombre_usuario in self.registros_usuarios:
            print("El nombre de usuario ya existe. Por favor, elija otro.")
            return
        contraseña = input("Ingrese su contraseña: ")
        self.registros_usuarios[nombre_usuario] = contraseña
        print("Registro exitoso. Ahora puede iniciar sesión.")

    def guadar_usuarios(self):
        with open("usuarios.pickle", "wb") as f:
            pickle.dump(self.registros_usuarios,f)

    def cargar_usuarios(self):
        try:
            with open("usuarios.pickle", "rb") as f:
                self.registros_usuarios = pickle.load(f)
        except FileNotFoundError:
            pass

    def iniciar_sesion(self):
        print("Inicio de Sesión")
        nombre_usuario = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña: ")
        if nombre_usuario in self.registros_usuarios and self.registros_usuarios[nombre_usuario] == contraseña:
            print("Inicio de sesión exitoso. ¡Bienvenido!")
            return nombre_usuario
        else:
            print("Credenciales incorrectas. Inicio de sesión fallido.")
            return None

class EstacionMetroplus:
    def __init__(self):
        self.estaciones = [
            "Universidad de Medellín",
            "Los Alpes",
            "Estación La Palma",
            "Estación Parque de Belén",
            "Estación Rosales",
            "Estación Fátima",
            "Estación Nutibara",
            "Estación Industriales",
            "Estación Plaza Mayor",
            "Estación Cisneros",
            "Estación Minorista",
            "Estación Chagualo",
            "Estación Ruta N U de A",
            "Estación Hospital",
            "Estación San Pedro",
            "Estación Palos verdes",
            "Estación Gardel",
            "Estación Manrique",
            "Estación Las Esmeraldas",
            "Estación Berlín",
            "Parque de Aranjuez",
        ]
        self.bicicletas_disponibles = {
            "Bicicleta Normal": 5,
            "Bicicleta Eléctrica": 5,
            "Bicicleta con cajón": 5,
            "Bicicleta con silla para niños": 5,
        }
        self.precios = {
            "Bicicleta Normal": 4.000,
            "Bicicleta Eléctrica": 8.000,
            "Bicicleta con cajón": 5.000,
            "Bicicleta con silla para niños": 7.000,
        }

    def calcular_costo(self, tipo_bicicleta, hora_inicio, hora_fin):
        precios_por_hora =  {
            "Bicicleta Normal": 4.000,
            "Bicicleta Eléctrica": 8.000,
            "Bicicleta con cajón": 5.000,
            "Bicicleta con silla para niños": 7.000,
        }

        duracion = (hora_fin - hora_inicio).total_seconds()/ 3600

        costo_total = precios_por_hora[tipo_bicicleta] * duracion
        return costo_total

    def mostrar_estaciones(self):
        print("Estaciones de Metroplus:")
        for i, estacion in enumerate(self.estaciones, 1):
            print(f"{i}. {estacion}")

    def alquilar_bicicleta(self, usuario):
        self.mostrar_estaciones()
        estacion_elegida = int(input("Elija la estación (número) donde desea alquilar: ")) - 1
        
        if 0 <= estacion_elegida < len(self.estaciones):
            print(f"Ha elegido la estación {self.estaciones[estacion_elegida]}.")
            print("Tipos de bicicletas disponibles:")
            for i, (tipo, cantidad) in enumerate(self.bicicletas_disponibles.items(), 1):
                print(f"{i}. {tipo} - Disponibles: {cantidad} - Precio por hora: ${self.precios[tipo]}")

            tipo_elegido = int(input("Elija el tipo de bicicleta (número) que desea alquilar: ")) - 1

            if 0 <= tipo_elegido < len(self.bicicletas_disponibles):
                tipo_bicicleta = list(self.bicicletas_disponibles.keys())[tipo_elegido]

                if self.bicicletas_disponibles[tipo_bicicleta] > 0:
                    self.bicicletas_disponibles[tipo_bicicleta] -= 1
                    print(f"Alquiló una bicicleta {tipo_bicicleta} en la estación {self.estaciones[estacion_elegida]}.")
                    hora_inicio = datetime.datetime.now()

                    self.devolver_bicicleta(usuario, tipo_bicicleta, hora_inicio)

                    return tipo_bicicleta, hora_inicio
                else:
                    print(f"Lo sentimos, no hay bicicletas {tipo_bicicleta} disponibles en esta estación.")
            else:
                print("Opción inválida.")
        else:
            print("Estación inválida.")

    def devolver_bicicleta(self, usuario, tipo_bicicleta, hora_inicio):
        self.mostrar_estaciones()
        estacion_elegida = int(input("Elija la estación (número) donde desea devolver la bicicleta: ")) - 1

        if 0 <= estacion_elegida < len(self.estaciones):
            print(f"Ha elegido la estación {self.estaciones[estacion_elegida]}.")
            print("Tipos de bicicletas para devolver:")
            for i, (tipo, cantidad) in enumerate(self.bicicletas_disponibles.items(), 1):
                print(f"{i}. {tipo} - Disponibles: {cantidad}")

            tipo_elegido = int(input("Elija el tipo de bicicleta (número) que desea devolver: ")) - 1

            if 0 <= tipo_elegido < len(self.bicicletas_disponibles):
                tipo_bicicleta = list(self.bicicletas_disponibles.keys())[tipo_elegido]

                if self.bicicletas_disponibles[tipo_bicicleta] < 5:
                    hora_fin = datetime.datetime.now()
                    costo = self.calcular_costo(tipo_bicicleta, hora_inicio, hora_fin)
                    print(f"Devuelve la bicicleta {tipo_bicicleta} en la estación {self.estaciones[estacion_elegida]}.")
                    print(f"Costo total: ${costo}")
                    self.bicicletas_disponibles[tipo_bicicleta] += 1
                else:
                    print(f"No puedes devolver más bicicletas {tipo_bicicleta} en esta estación.")
            else:
                print("Opción inválida.")
        else:
            print("Estación inválida.")

if __name__ == '__main__':
    usuarios = Usuarios()
    estacion_metroplus = EstacionMetroplus()

    usuarios.cargar_usuarios()
    usuario_actual = None

    while True:
        print("\nOpciones:")
        if usuario_actual is None:
            print("1. Registrar Usuario")
            print("2. Iniciar Sesión")
        else:
            print(f"Bienvenido, {usuario_actual}!")
            print("3. Alquilar Bicicleta")
            print("4. Devolver Bicicleta")
            print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if usuario_actual is None:
            if opcion == '1':
                usuarios.registrar_usuario()
                usuarios.guadar_usuarios()
            elif opcion == '2':
                usuario_actual = usuarios.iniciar_sesion()
                if usuario_actual is None:
                    print("Inicio de sesión fallido. Por favor, intente nuevamente.")
        else:
            if opcion == '3':
                estacion_metroplus.alquilar_bicicleta(usuario_actual)
            elif opcion == '4':
                estacion_metroplus.devolver_bicicleta()
            elif opcion == '5':
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
