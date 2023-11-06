import tkinter as tk
from tkinter import messagebox
import datetime
from proyecto import Usuarios
from proyecto import EstacionMetroplus

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro e Inicio de Sesión")
        self.usuario_actual = None

        self.usuarios = Usuarios()
        self.estacion_metroplus = EstacionMetroplus()
        self.usuarios.cargar_usuarios()

        self.create_widgets()

    def calcular_costo(self, tipo_bicicleta, hora_inicio, hora_fin):
        precios_por_hora = {
            "Bicicleta Normal": 4000,
            "Bicicleta Eléctrica": 8000,
            "Bicicleta con cajón": 5000,
            "Bicicleta con silla para niños": 7000,
        }

        if tipo_bicicleta in precios_por_hora:
            tarifa_por_hora = precios_por_hora[tipo_bicicleta]
            duracion = (hora_fin - hora_inicio).total_seconds() / 3600 
            costo_total = tarifa_por_hora * duracion
            return costo_total
        else:
            return 0

    def update_ui(self):
        self.frame.destroy()  
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        if self.usuario_actual is None:
            self.label = tk.Label(self.frame, text="Opciones:")
            self.label.pack()

            self.username_label = tk.Label(self.frame, text="Nombre de Usuario:")
            self.username_label.pack()
            self.username_entry = tk.Entry(self.frame)
            self.username_entry.pack()

            self.password_label = tk.Label(self.frame, text="Contraseña:")
            self.password_label.pack()
            self.password_entry = tk.Entry(self.frame, show="*")
            self.password_entry.pack()

            self.register_button = tk.Button(self.frame, text="Registrar Usuario", command=self.registrar_usuario)
            self.register_button.pack()

            self.login_button = tk.Button(self.frame, text="Iniciar Sesión", command=self.iniciar_sesion)
            self.login_button.pack()
        else:
            self.show_bike_buttons()

    def registrar_usuario(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if username in self.usuarios.registros_usuarios:
                messagebox.showerror("Error", "El nombre de usuario ya existe. Por favor, elija otro.")
            else:
                self.usuarios.registros_usuarios[username] = password
                self.usuarios.guadar_usuarios()
                messagebox.showinfo("Registro exitoso", "Registro exitoso. Ahora puede iniciar sesión.")
        else:
            messagebox.showerror("Error", "Debe ingresar un nombre de usuario y una contraseña.")

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        if self.usuario_actual is None:
            self.label = tk.Label(self.frame, text="Opciones:")
            self.label.pack()

            self.username_label = tk.Label(self.frame, text="Nombre de Usuario:")
            self.username_label.pack()
            self.username_entry = tk.Entry(self.frame)
            self.username_entry.pack()

            self.password_label = tk.Label(self.frame, text="Contraseña:")
            self.password_label.pack()
            self.password_entry = tk.Entry(self.frame, show="*")
            self.password_entry.pack()

            self.register_button = tk.Button(self.frame, text="Registrar Usuario", command=self.registrar_usuario)
            self.register_button.pack()

            self.login_button = tk.Button(self.frame, text="Iniciar Sesión", command=self.iniciar_sesion)
            self.login_button.pack()
        else:
            self.show_bike_buttons()
       

    def iniciar_sesion(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if username in self.usuarios.registros_usuarios and self.usuarios.registros_usuarios[username] == password:
                self.usuario_actual = username
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                self.update_ui()
                messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso. ¡Bienvenido!")
            else:
                messagebox.showerror("Error", "Credenciales incorrectas. Inicio de sesión fallido.")
        else:
            messagebox.showerror("Error", "Debe ingresar un nombre de usuario y una contraseña.")
    def show_bike_buttons(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.welcome_label = tk.Label(self.frame, text=f"Bienvenido, {self.usuario_actual}!")
        self.welcome_label.pack()

        self.rent_button = tk.Button(self.frame, text="Alquilar Bicicleta", command=self.alquilar_bicicleta)
        self.rent_button.pack()

        self.return_button = tk.Button(self.frame, text="Devolver Bicicleta", command=self.devolver_bicicleta)
        self.return_button.pack()

        self.exit_button = tk.Button(self.frame, text="Salir", command=self.root.quit)
        self.exit_button.pack()


    def alquilar_bicicleta(self):
        if self.usuario_actual:
            self.frame.destroy()
            self.create_rental_menu()
        else:
            messagebox.showerror("Error", "Debe iniciar sesión para alquilar una bicicleta.")

    def create_rental_menu(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.station_label = tk.Label(self.frame, text="Selecciona una estación:")
        self.station_label.pack()

        self.station_options = tk.StringVar(value=self.estacion_metroplus.estaciones)
        self.station_menu = tk.OptionMenu(self.frame, self.station_options, *self.estacion_metroplus.estaciones)
        self.station_menu.pack()

        self.bike_label = tk.Label(self.frame, text="Selecciona un tipo de bicicleta:")
        self.bike_label.pack()

        self.bike_options = tk.StringVar(value=list(self.estacion_metroplus.bicicletas_disponibles.keys()))
        self.bike_menu = tk.OptionMenu(self.frame, self.bike_options, *list(self.estacion_metroplus.bicicletas_disponibles.keys()))
        self.bike_menu.pack()

        self.rent_confirm_button = tk.Button(self.frame, text="Confirmar Alquiler", command=self.confirmar_alquiler)
        self.rent_confirm_button.pack()

        self.back_button = tk.Button(self.frame, text="Volver al Menú Principal", command=self.update_ui)
        self.back_button.pack()

    def confirmar_alquiler(self):
        estacion_elegida = self.station_options.get()
        tipo_bicicleta = self.bike_options.get()

        if estacion_elegida and tipo_bicicleta:
            estacion_index = self.estacion_metroplus.estaciones.index(estacion_elegida)
            if self.estacion_metroplus.bicicletas_disponibles[tipo_bicicleta] > 0:
                self.estacion_metroplus.bicicletas_disponibles[tipo_bicicleta] -= 1
                hora_inicio = datetime.datetime.now()
                
                messagebox.showinfo("Alquiler Exitoso", f"Has alquilado una bicicleta {tipo_bicicleta} en la estación {estacion_elegida}.")
                self.update_ui()
            else:
                messagebox.showerror("Error", f"No hay bicicletas {tipo_bicicleta} disponibles en esta estación.")
        else:
            messagebox.showerror("Error", "Debes seleccionar una estación y un tipo de bicicleta.")

    def devolver_bicicleta(self):
        if self.usuario_actual:
            self.frame.destroy()
            self.create_return_menu()
        else:
            messagebox.showerror("Error", "Debe iniciar sesión para devolver una bicicleta.")

    def create_return_menu(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.return_station_label = tk.Label(self.frame, text="Selecciona la estación para devolver la bicicleta:")
        self.return_station_label.pack()

        self.return_station_options = tk.StringVar(value=self.estacion_metroplus.estaciones)
        self.return_station_menu = tk.OptionMenu(self.frame, self.return_station_options, *self.estacion_metroplus.estaciones)
        self.return_station_menu.pack()

        self.return_confirm_button = tk.Button(self.frame, text="Confirmar Devolución", command=self.confirmar_devolucion)
        self.return_confirm_button.pack()

        self.return_back_button = tk.Button(self.frame, text="Volver al Menú Principal", command=self.update_ui)
        self.return_back
        
    def devolver_bicicleta(self):
        if self.usuario_actual:
            self.frame.destroy()
            self.create_return_menu()
        else:
            messagebox.showerror("Error", "Debe iniciar sesión para devolver una bicicleta.")

    

    def confirmar_devolucion(self):
        estacion_elegida = self.return_station_options.get()
        tipo_bicicleta = self.bike_options.get()

        if estacion_elegida:
            estacion_index = self.estacion_metroplus.estaciones.index(estacion_elegida)
            if self.estacion_metroplus.bicicletas_disponibles[tipo_bicicleta] < 5:
                self.estacion_metroplus.bicicletas_disponibles[tipo_bicicleta] -= 1
                hora_inicio = datetime.datetime.now()
                hora_fin = datetime.datetime.now()
            
                costo = self.estacion_metroplus.calcular_costo(tipo_bicicleta, hora_inicio, hora_fin)
            
                self.estacion_metroplus.bicicletas_disponibles[tipo_bicicleta] += 1
            
                resultado = f"Has devuelto la bicicleta {tipo_bicicleta} en la estación {estacion_elegida}.\nCosto total: ${costo}"
                messagebox.showinfo("Devolución Exitosa", resultado)

                
                self.return_to_main_button = tk.Button(self.frame, text="Volver al Menú Principal", command=self.update_ui)
                self.return_to_main_button.pack()
            else:
                messagebox.showerror("Error", "No puedes devolver más bicicletas en esta estación.")
        else:
            messagebox.showerror("Error", "Debes seleccionar una estación.")


            self.precios_por_hora = {
                "Bicicleta Normal": 4000,
                "Bicicleta Eléctrica": 8000,
                "Bicicleta con cajón": 5000,
                "Bicicleta con silla para niños": 7000,
            }
    def calcular_costo(self, tipo_bicicleta, duracion):
        if tipo_bicicleta in precios_por_hora:
            tarifa_por_hora = precios_por_hora[tipo_bicicleta]
            costo_total = tarifa_por_hora * (duracion.total_seconds() / 3600)
            return costo_total
        else:
            return 0


    def create_return_menu(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.return_station_label = tk.Label(self.frame, text="Selecciona la estación de devolución:")
        self.return_station_label.pack()

        self.return_station_options = tk.StringVar(value=self.estacion_metroplus.estaciones)
        self.return_station_menu = tk.OptionMenu(self.frame, self.return_station_options, *self.estacion_metroplus.estaciones)
        self.return_station_menu.pack()

        self.return_bike_label = tk.Label(self.frame, text="Selecciona el tipo de bicicleta:")
        self.return_bike_label.pack()

        self.return_bike_options = tk.StringVar(value=list(self.estacion_metroplus.bicicletas_disponibles.keys()))
        self.return_bike_menu = tk.OptionMenu(self.frame, self.return_bike_options, *list(self.estacion_metroplus.bicicletas_disponibles.keys()))
        self.return_bike_menu.pack()

        self.return_confirm_button = tk.Button(self.frame, text="Confirmar Devolución", command=self.confirmar_devolucion)
        self.return_confirm_button.pack()

        self.return_to_main_button = tk.Button(self.frame, text="Volver al Menú Principal", command=self.update_ui)
        self.return_to_main_button.pack()

    def update_ui(self):
        self.frame.destroy()
        self.create_widgets()

if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()