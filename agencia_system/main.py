#AQUI ESTAN LOS MENUS DE OPCIONES

from Personas import usuarios  #importacion de modulos y paquetes
from Servicios import servicios
import getpass
from funciones import * #usamos limpiar pantalla y esperar tecla
from conexionBD import obtener_conexion #conectamos a la bd en algunos momeno

#MENUS DIFERENTES PARA CADA ACCION
def menu_inicial():
    while True:
        limpiarPantalla()
        print("""
             ....::::::Sistema Gestion de Beneficiarios::::::....
          
          1- Registrarse
          2- Iniciar Sesion
          3- Salir

        """)
        opcion=input("Eliga una opcion: ").upper()

        if opcion == '1' or opcion == 'REGISTRARSE':
            # Pedir datos
            limpiarPantalla()
            print("\n \t ..:: Registro en el Sistema ::..")
            print("Ingrese lo que se le pida: ")
            nombre = input("\t Nombre: ")
            apellidos = input("\t Apellidos: ")
            edad = input("\t Edad: ")
            tel = input("\t Teléfono: ")
            direccion = input("\t Dirección: ")
            email = input("\t Ingresa un correo válido: ")
            password = getpass.getpass("\t Ingresa una contraseña: ")

            # Validar datos de entrada
            if not all([nombre, apellidos, edad, tel, direccion, email, password]):
                print("Todos los campos deben ser completados.")
            else:
                # Creación de instancia de la clase Clientes con todos los datos
                obj_usuario = usuarios.Clientes(None, nombre, apellidos, edad, tel, email, password, direccion)
                
                # Registrar usuario
                cliente_id = obj_usuario.registrar(nombre, apellidos, edad, tel, direccion, email, password)
                esperarTecla()

        elif opcion == '2' or opcion == 'INICIO SESION':
            # Pedir datos de inicio de sesión
            limpiarPantalla()
            print("\n \t ..:: Inicio de Sesión ::..")
            email = input("\t Ingresa tu correo electrónico: ")
            password = getpass.getpass("\t Ingresa tu contraseña: ")

            # Validar datos de entrada
            if not all([email, password]):
                print("Correo electrónico y contraseña deben ser completados.")
            else:
                # Creación de instancia de la clase Personas para iniciar sesión
                obj_usuario = usuarios.Personas(None, None, None, None, None, email, password)  # Solo correo y contraseña necesarios
                
                tipo_usuario, usuario_id = obj_usuario.iniciar_sesion(email, password)

                if tipo_usuario == 'cliente':
                    menu_cliente(usuario_id)  # Pasa el id del cliente

                elif tipo_usuario == 'empleado':
                    menu_empleado(usuario_id)  # Pasa el id del empleado

                else:
                    esperarTecla()





        elif opcion == '3' or opcion == 'SALIR':
            print("¡Que tenga un buen día!...Ha salido del sistema")
            break
        else:
            print("\t Opcion no váida....Porfavor intente de nuevo")
            esperarTecla()


def menu_empleado(empleado_id):
    while True:
        limpiarPantalla()
        print("""
        .....:::::¡Bienvenido, Empleado!:::::...
          1) Atender Solicitudes
          2) Mis Datos
          3) Actualizar Datos
          4) Regresar
        """)
        opcion = input("Eliga una opción: ").strip()

        if opcion == '1':
            #ATENDER SOLICITUDES
            limpiarPantalla()
            print("¡He aqui las Solicitudes que lo requieren!")
            #Mostrar las solicitudes pendientes
            obj_solicitud = usuarios.Empleados(None, None, None, None, None, None, None, None, None, None, None, None)
            obj_solicitud.mostrar_solicitudes_empleado(empleado_id)

            #Atender soicitudes
            keso = True
            while keso:
                print("")
                solicitud_id = input("Ingrese el ID de la solicitud (o 'salir' para cancelar): ")

                # Verificar si el usuario desea salir del bucle
                if solicitud_id.upper() == 'SALIR':
                    print("Cancelando operación...")
                    break

                # Verificar que solicitud_id no esté vacío y sea un número entero
                if not solicitud_id.isdigit(): #esto verifica si lo ingresado es entero
                    print("Error: El ID de la solicitud debe ser un número válido.")
                    continue #continuaa

                print("")
                opcion = input("¿Desea agendarle una cita a esta solicitud? (SI/NO): ").upper()

                if opcion in ['SI', 'YES', 'S']:
                    print("")
                    obj_solicitud.programar_cita(empleado_id, int(solicitud_id))
                    keso = False  # salir del bucle

                elif opcion in ['NO', 'N']:
                    print("")
                    opcion1 = input("¿Desea rechazar esta solicitud? (SI/NO): ").upper()
                    if opcion1 in ['SI', 'YES', 'S']:
                        # Rechazar solicitud
                        obj_solicitud.atender_solicitud(int(solicitud_id), 'Rechazada')
                        keso = False  # salir del bucle
                else:
                    print("Opción no válida... vuelva a intentarlo")

                esperarTecla()

        elif opcion == '2' or opcion == 'MOSTRAR':
            #MOSTRAR DATOS
            limpiarPantalla()
            print("\t\t ¡Sus Datos Personales!")
            print("")
            #Crear una instancia de la clase 
            obj_empleado=usuarios.Empleados(None, None, None, None, None, None, None, None, None, None, None, None)
            obj_empleado.mostrar_datos(empleado_id)
            esperarTecla()
            

        elif opcion == '3':
            limpiarPantalla()
            print("¡Actualizará sus datos personales!")
            #intancia de clase
            obj_empleado = usuarios.Empleados(None, None, None, None, None, None, None, None, None, None, None, None)
            obj_empleado.actualizar_datos(empleado_id)
            esperarTecla()


        elif opcion == '4':

            break
        else:
            print("Opción no válida, intente nuevamente.")
            esperarTecla()





def menu_cliente(cliente_id):
    # Obtener el nombre del cliente usando el cliente_id
    obj_cliente = usuarios.Clientes(None, None, None, None, None, None, None, None)
    nombre = obj_cliente.obtener_nombre_cliente(cliente_id)
    while True:
        limpiarPantalla()
        print(f"""
        .....:::::¡Bienvenido {nombre} !:::::...
          1) Mostrar Agencias 
          2) Servicios disponibles
          3) Mi perfil
          4) Solicitar Servicio
          5) Citas
          6) Regresar
        """)

        opcion = input("Eliga una opción: ").upper()

        if opcion == '1':
            #MOSTRAR AGENCIAS DISPONIBLES
            limpiarPantalla()
            print("\t\t¡He aqui todas las agencias disponibles!")
            print("")
            # Crear una instancia de Agencias y mostrar detalles
            obj_agencia = servicios.Agencias(None, None, None, None, None)
            obj_agencia.mostrar_detalles()
            esperarTecla()


        elif opcion == '2':
            #SERVICIOS DISPONIBLES
            limpiarPantalla()
            print("\t\t¡Servicios Disponibles!")
            print("")
            obj_service = servicios.Servicios(None, None, None, None, None)
            obj_service.mostrar_servicios()
            esperarTecla()

        elif opcion == '3':
            # MI PERFIL
            menu_perfil(cliente_id)

        elif opcion == '4':
            # SOLICITAR SERVICIO (agregar solicitud)
            limpiarPantalla()
            print("..::::Solicitud de Servicio::::..")
            print("")
            id_servicio = input("Ingrese el ID del servicio: ")  
            documentos = input("Ingrese documentos necesarios (opcional): ")
            comentarios = input("Ingrese comentarios adicionales (opcional): ")
            
            # Llamar a la función para registrar la solicitud
            obj_service = usuarios.Clientes(None, None, None, None, None, None, None, None)
            obj_service.solicitar_servicio(id_servicio, cliente_id, documentos, comentarios)
            
            esperarTecla()

        elif opcion == '5':
            menu_citas(cliente_id)


        elif opcion == '6' or opcion=='REGRESAR':
            break

        else:
            print("Opción no válida.... por favor intente de nuevo")
            esperarTecla()



def menu_perfil(cliente_id):
     while True:
        limpiarPantalla()
        print("""
        .....:::::Mi Perfil:::::...
          1) Mis Datos
          2) Actualizar Datos
          3) Mis Solicitudes
          4) Regresar
        """)
        opcion=input("Eliga una opcion: ").upper()

        if opcion == '1' or opcion == 'MOSTRAR':
            #MOSTRAR DATOS
            limpiarPantalla()
            print("\t\t ¡Sus Datos Personales!")
            print("")
            #Crear una instancia de la clase 
            obj_cliente=usuarios.Clientes(None, None, None, None, None, None, None, None)
            obj_cliente.mostrar_datos(cliente_id)
            esperarTecla()
            

        elif opcion == '2' or opcion == 'ACTUALIZAR':
            limpiarPantalla()
            print("\t\t ¡Puedes modificar los datos que ingresaste al registrarse!")
            print("")
            #Crear una instancia de la clase 
            obj_cliente=usuarios.Clientes(None, None, None, None, None, None, None, None)
            obj_cliente.actualizar_datos(cliente_id)
            esperarTecla()

        elif opcion == '3':
            #MIS SOLICITUDES
            menu_solicitudes(cliente_id)
        elif opcion == '4' or opcion == 'REGRESAR':
            print("")
            break
        else:
            print("Opcion no válida.... porfavor intente de nuevo")
            esperarTecla()

     

def menu_citas(cliente_id):
    while True:
        limpiarPantalla()
        print("""
        .....:::::Mi Gestion de Citas:::::...
          1) Mostrar Citas Programadas
          2) Confirmar Cita
          3) Cancelar Cita
          4) Regresar
        """)
        opcion=input("Eliga una opcion: ").upper()

        if opcion == '1' or opcion == 'MOSTRAR':
            #MOSTRAR CITAS
            limpiarPantalla()
            print("\t\t ¡Citas programadas para usted!")
            print("")
            #Crear una instancia de la clase 
            obj_cita = servicios.Citas(None, None, None, None, None, None)
            obj_cita.mostrar_citas(cliente_id)
            esperarTecla()
            

        elif opcion == '2' or opcion == 'CONFIRMAR':
            #CONFIRMAR CITAS
            limpiarPantalla()
            print("¡Confirmarás una cita!")
            cita_id = input("Ingrese el ID de la cita a confirmar: ")
            #creacion de instancias de clases
            obj_cita = servicios.Citas(None, None, None, None, None, None)
            obj_cita.confirmar(cita_id)
            esperarTecla()

        elif opcion == '3' or opcion == 'CANCELAR':
            #CANCELAR CITAS
            limpiarPantalla()
            print("Cncelarás una cita!")
            cita_id = input("Ingrese el ID de la cita a cancelar: ")
            #creacion de instancias de clases
            obj_cita = servicios.Citas(None, None, None, None, None, None)
            obj_cita.cancelar_cita(cita_id)
            esperarTecla()

        elif opcion == '4' or opcion == 'REGRESAR':
            print("")
            break
        else:
            print("Opcion no válida.... porfavor intente de nuevo")
            esperarTecla()



def menu_solicitudes(cliente_id):
    while True:
        limpiarPantalla()
        print("""
        .....:::::Mis Solicitudes:::::...
            1) Ver Solicitudes
            2) Eiminar Solicitudes
            3) Regresar
        """)
        opcion=input("Eliga una opcion: ").upper()

        if opcion == '1':
            #MOATRAR SOLICITUDES
            limpiarPantalla()
            print("¡Mostraré todas sus solicitudes!")
            #instancias de la clase
            obj_solicitud = servicios.Solicitudes(None, None, None, None, None, None, None)
            obj_solicitud.mostrar_solicitudes(cliente_id)
            esperarTecla()


        elif opcion == '2':
            #ELIMINAR SOLICITUDES
            limpiarPantalla()
            print("¡Eliminará una solicitud!")
            solicitud_id = input("Ingrese el ID de la solicitud que desea eliminar: ")
            #instancias de la clase
            obj_solicitud = usuarios.Clientes(None, None, None, None, None, None, None, None)
            obj_solicitud.eliminar_solicitud(solicitud_id, cliente_id)
            esperarTecla()

        elif opcion == '3':
            break

        else:
            print("Ingresó una opcion incorrecta...intentelo de nuevo")
            esperarTecla()





#aqui le dice al pitón que ejecute primero el menu_inicial()
if __name__ == "__main__":
    menu_inicial()


