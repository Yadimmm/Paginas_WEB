# CLASES DE LAS PERSONAS
#paquete ´Personas'
#usuario.py
from conexionBD import obtener_conexion
from funciones import * 
import hashlib
import datetime
from datetime import datetime
from mysql.connector import Error

class Personas:
    def __init__(self, usuario, nombre, apellidos, edad, telefono, correo, password):
        self.__usuario = usuario
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__edad = edad
        self.__telefono = telefono
        self.__correo = correo
        self.contrasena = self.hash_password(password) if password else None   #hashear password y guardar en contrasena

    # GETTER Y SETTER
    def getIdentificador(self):
        return self.__usuario

    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre = nombre

    def getApellidos(self):
        return self.__apellidos

    def setApellidos(self, apellidos):
        self.__apellidos = apellidos

    def getEdad(self):
        return self.__edad

    def setEdad(self, edad):
        self.__edad = edad

    def getTelefono(self):
        return self.__telefono

    def setTelefono(self, telefono):
        self.__telefono = telefono

    def getCorreo(self):
        return self.__correo

    def setCorreo(self, correo):
        self.__correo = correo

    # FUNCION DE LA PERSONA

    def hash_password(self, contrasena):
        if contrasena:  # Asegúrate de que contrasena no sea None
            return hashlib.sha256(contrasena.encode()).hexdigest()
        return None


    def verificar_password(self, password_ingresada, password_almacenada):
        return self.hash_password(password_ingresada) == password_almacenada

    def iniciar_sesion(self, email, password):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()

                # Verificar si el usuario es un cliente
                cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
                cliente = cursor.fetchone()

                # Si no es cliente, verificar si es empleado
                if not cliente:
                    cursor.execute("SELECT * FROM empleados WHERE email = %s", (email,))
                    empleado = cursor.fetchone()
                    
                    if empleado:
                        password_almacenada = empleado[7]  # Index de la contraseña en la tabla empleados
                        if self.verificar_password(password, password_almacenada):
                            return 'empleado', empleado[0]
                    else:
                        print("Usuario no encontrado.")
                        return None, None
                else:
                    password_almacenada = cliente[7]  # Index de la contraseña en la tabla clientes
                    if self.verificar_password(password, password_almacenada):
                        return 'cliente', cliente[0]
                    else:
                        print("Credenciales incorrectas.")
                        return None, None

            except Exception as e:
                print(f"Error al iniciar sesión: {e}")
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()
        else:
            print("No se pudo establecer conexión a la base de datos.")
        return None, None



    

            



class Clientes(Personas):
    def __init__(self, usuario, nombre, apellidos, edad, telefono, correo, password, direccion):
        super().__init__(usuario, nombre, apellidos, edad, telefono, correo, password)
        self.__direccion = direccion

    # GETTER Y SETTER

    def getDireccion(self):
        return self.__direccion

    def setDireccion(self, direccion):
        self.__direccion = direccion


    # FUNCION PARA CLIENTES
    
    def registrar(self, nombre, apellidos, edad, telefono, direccion, correo, contrasena):
        
        conexion = obtener_conexion()
        try:
            if conexion:
                cursor = conexion.cursor()
                hashed_password = self.hash_password(contrasena) if contrasena else None  # Hashear la contraseña
                cursor.execute(
                    "INSERT INTO clientes (nombre, apellidos, edad, tel, direccion, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (nombre, apellidos, edad, telefono, direccion, correo, hashed_password)
                )
                conexion.commit()
                cliente_id = cursor.lastrowid
                print(f"Se ha registrado con éxito, su usuario es: {cliente_id}")
                return cliente_id
            else:
                print("No se pudo establecer la conexión a la base de datos.")
                return None
        except Exception as e:
            print(f"Error al registrar el cliente: {e}")
            return None
        finally:
            if conexion:
                cursor.close()
                conexion.close()

                
                

    def mostrar_datos(self, id_cliente):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, nombre, apellidos, edad, tel, direccion, email FROM clientes WHERE id = %s", (id_cliente,))
                for (id, nombre, apellidos, edad, telefono,direccion, correo) in cursor: #iterar para imprimir bonito
                    print("")
                    print(f"Usuario: {id}\n Nombre: {nombre} \n Apellidos: {apellidos}\n Edad:{edad}\n Teléfono: {telefono}\n Dirección: {direccion}\n E-mail: {correo}\n Password: ****** ")
               

            except Exception as e:
                print(f"Error al obtener los datos del cliente: {e}")
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()
        else:
            print("No se pudo establecer la conexión a la base de datos.")
        


    def obtener_nombre_cliente(self, cliente_id):
        conexion = obtener_conexion()
        nombre = ""
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "SELECT nombre FROM clientes WHERE id = %s"
                cursor.execute(query, (cliente_id,))
                resultado = cursor.fetchone()
                if resultado:
                    nombre = resultado[0]
                else:
                    print("Cliente no encontrado.")
            except Error as e:
                print(f"Error al obtener el nombre del cliente: {e}")
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()
        return nombre



    def actualizar_datos(self, id_cliente):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            
            # Buscar el cliente que eligió
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
            resultado = cursor.fetchone()

            if resultado:
                nombre_actual, apellido_actual, edad_actual, telefono_actual, direccion_actual, correo_actual, contrasena_almacenada = resultado[1:]

                # Solicitar nuevos datos
                limpiarPantalla()
                print("Presione Enter para dejar sin cambios")
                nombre = input(f"Nombre ({nombre_actual}): ") or nombre_actual
                apellidos = input(f"Apellidos ({apellido_actual}): ") or apellido_actual
                edad = input(f"Edad ({edad_actual}): ") or edad_actual
                telefono = input(f"Teléfono ({telefono_actual}): ") or telefono_actual
                direccion = input(f"Dirección ({direccion_actual}): ") or direccion_actual
                correo = input(f"Correo ({correo_actual}): ") or correo_actual
                password = input(f"Contraseña (dejar en blanco para no cambiar): ")

                # Hash de la nueva contraseña si se proporciona
                if password:
                    obj_cliente = Clientes(...)  # Instanciar la clase con los datos necesarios
                    password = obj_cliente.hash_password(password)

                # Convertir edad a entero si es necesario
                if edad:
                    edad = int(edad)

                # Actualizar datos del cliente
                cursor.execute("""
                    UPDATE clientes
                    SET nombre = %s, apellidos = %s, edad = %s, tel = %s, direccion = %s, email = %s, password = %s
                    WHERE id = %s
                """, (nombre, apellidos, edad, telefono, direccion, correo, password if password else contrasena_almacenada, id_cliente))
                
                conexion.commit()
                
                print(f"Datos actualizados correctamente.")
            else:
                print("Cliente no encontrado.")
                
        except Exception as e:
            limpiarPantalla()
            print(f"Ocurrió un error al actualizar sus datos: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def eliminar_solicitud(self, solicitud_id, id_cliente):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                
                # Verificar si la solicitud existe
                cursor.execute("SELECT * FROM solicitudes WHERE id = %s AND cliente_id = %s", (solicitud_id, id_cliente))
                if cursor.fetchone():
                    cursor.execute("DELETE FROM solicitudes WHERE id = %s", (solicitud_id,))
                    conexion.commit()
                    print("Solicitud eliminada correctamente.")
                else:
                    print("No se encontró la solicitud o no pertenece a su cuenta.")
                    
            except Exception as e:
                print(f"Error al eliminar la solicitud: {e}")
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()
            

    def solicitar_servicio(self, id_servicio, id_cliente, documentos, comentarios):
        # Obtener la fecha y hora actuales
        fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                #sacar el empleado_id de la tabla servicios
                cursor.execute("SELECT empleado_id, agencia_id FROM servicios WHERE id = %s",(id_servicio,))
                resultado = cursor.fetchone()
                id_empleado=resultado[0] #posicion de la tupla es el id de empleado que atiende e servicio
                id_agencia=resultado[1] #posicion de la tupla es el id de agencia que atiende e servicio
                query = ("INSERT INTO solicitudes "
                        "(servicio_id, empleado_id, cliente_id, agencia_id, fecha_solicitud, estado, documentos, comentarios) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                values = (id_servicio, id_empleado, id_cliente, id_agencia, fecha_solicitud, 'Pendiente', documentos, comentarios)
                cursor.execute(query, values)
                conexion.commit()
                print("Solicitud registrada con éxito.")
            except Error as e:
                print(f"Error al registrar la solicitud: {e}")
            finally:
                cursor.close()
                conexion.close()






class Empleados(Personas):
    def __init__(self, usuario, nombre, apellidos, edad, telefono, correo, password, puesto, titulo, salario, fecha_nacimiento, id_agencia):
        super().__init__(usuario, nombre, apellidos, edad, telefono, correo, password)
        self.__puesto = puesto
        self.__titulo=titulo
        self.__salario = salario
        self.fecha_nacimiento = fecha_nacimiento
        self.id_agencia = id_agencia
        

    # GETTER Y SETTER
    def getPuesto(self):
        return self.__puesto

    def setPuesto(self, puesto):
        self.__puesto = puesto

    def getTitulo(self):
        return self.__titulo

    def setTitulo(self, titulo):
        self.__titulo = titulo

    def getSalario(self):
        return self.__salario

    def setSalario(self, salario):
        self.__salario = salario

    

    # FUNCIONES DE EMPLEADOS

    @staticmethod 
    def atender_solicitud(self, id_solicitud, nuevo_estado): #aqui que o que
         #de hecho estas rechazando mana
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "UPDATE solicitudes SET estado = %s WHERE id = %s"
                cursor.execute(query, (nuevo_estado, id_solicitud))
                conexion.commit()
                print("La solicitud ha sido rechazada con éxito")
            except Error as e:
                print(f"Error al rechazar la solicitud: {e}")
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()



    def mostrar_datos(self, empleado_id):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("select * from empleados where id = %s",(empleado_id,))
            for (empleado_id, nombre, apellidos, edad, fecha_nacimiento, telefono, correo, password, puesto, titulo, salario, id_agencia) in cursor: #iterar para imprimir bonito
                print("")
                print(f"Usuario: {empleado_id}\n Nombre: {nombre} {apellidos}\n Edad: {edad}\n Fecha de nacimiento: {fecha_nacimiento} \n Teléfono: {telefono} \n Correo: {correo}\n Puesto: {puesto}\n Titulo: {titulo} \n Salario: {salario} \n Agencia: {id_agencia} ")
            cursor.close()
            conexion.close()
        else:
            print("No se pudo establecer la conexión a la base de datos.")


    
    def programar_cita(self, empleado_id, solicitud_id):
    
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                # Verificar si la solicitud existe y está pendiente
                cursor.execute("SELECT cliente_id FROM solicitudes WHERE id = %s AND estado = 'Pendiente'", (solicitud_id,))
                solicitud = cursor.fetchone()
                
                if solicitud:
                    cliente_id = solicitud[0]  # ahi ta el ciente yayaya
                    fecha_cita = input("Ingrese la fecha y hora de la cita (YYYY-MM-DD HH:MM:SS): ")
                    
                    query = """
                        INSERT INTO citas (cliente_id, solicitud_id, empleado_id, fecha_cita, estado)
                        VALUES (%s, %s, %s, %s, 'Pendiente')
                    """
                    cursor.execute(query, (cliente_id, solicitud_id, empleado_id, fecha_cita))
                    conexion.commit()
                    
                    # Actualizar el estado de la solicitud a 'Aprobada'
                    cursor.execute("UPDATE solicitudes SET estado = 'Aprobada' WHERE id = %s", (solicitud_id,))
                    conexion.commit()
                    
                    print("Cita programada con éxito.")
                else:
                    print("Solicitud no encontrada o ya no está pendiente.")
            except Exception as e:
                print(f"Error al programar la cita: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conexion:
                    conexion.close()



    def actualizar_datos(self, id_empleado):
        # Verificar si el empleado existe
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            
            # Mostrar el empleado que eligió
            cursor.execute("SELECT * FROM empleados WHERE id = %s", (id_empleado,))
            resultado = cursor.fetchone()

            if not resultado:
                limpiarPantalla()
                print(f"No existe el empleado con el ID {id_empleado}.")
            else:
                # Almacenar datos actuales en caso de dar enter
                nombre_actual, apellido_actual, edad_actual, fecha_actual, telefono_actual, correo_actual, password_actual, puesto_actual, titulo_actual, salario_actual, id_agencia_actual = resultado[1:]

                # Solicitar nuevos datos
                limpiarPantalla()
                print("Presione Enter para dejar sin cambios")
                nombre = input(f"Nombre ({nombre_actual}): ") or nombre_actual
                apellidos = input(f"Apellidos ({apellido_actual}): ") or apellido_actual
                edad = input(f"Edad ({edad_actual}): ") or edad_actual
                fecha_nacimiento = input(f"Fecha de nacimiento ({fecha_actual}): ") or fecha_actual
                telefono = input(f"Teléfono ({telefono_actual}): ") or telefono_actual
                correo = input(f"Correo ({correo_actual}): ") or correo_actual
                puesto = input(f"Puesto ({puesto_actual}): ") or puesto_actual
                titulo = input(f"Titulo ({titulo_actual}): ") or titulo_actual

                id_agencia_input = input(f"Ingrese el ID de la agencia ({id_agencia_actual}): ") #aqui tambien
                if id_agencia_input:
                    try:
                        id_agencia = int(id_agencia_input) #lo convierte entero si agrego numeros
                    except ValueError:
                        limpiarPantalla()
                        print("Error: El ID de la agencia debe ser un número válido. Se mantendrá el ID de la agencia actual.")
                        id_veterinaria = id_veterinaria_actual #guarda e actual
                else:
                    id_agencia = id_agencia_actual #si presiona enter se mantiene con la id actual
                    #todo esto pasa cuando manejamos valores tipo INT y al presionar enter manda error
                    # ya sabes, quiere recibir valores numericos y el enter no ayuda

                # Proceder a actualizar los detalles del empleado
                #AQUI VAMOOOS
                cursor.execute("""
                    UPDATE empleados
                    SET nombre = %s, apellidos = %s, edad = %s, fecha_nacimiento =%s, telefono = %s, email = %s, puesto = %s, titulo = %s, agencia_id = %s
                    WHERE id = %s
                """, (nombre, apellidos, edad, fecha_nacimiento, telefono, correo, puesto, titulo, id_agencia, id_empleado))
                
                conexion.commit()
                limpiarPantalla()
                print(f"Datos del empleado con ID {id_empleado} actualizados correctamente.")
                
        except Exception as e:
            limpiarPantalla()
            print(f"Ocurrió un error al actualizar los datos del empleado: {e}") #pipipipip
        finally:
            if conexion:
                cursor.close()
                conexion.close() #cierra todo, es buena practica mana



    def mostrar_solicitudes_empleado(self, empleado_id):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                # Consulta para obtener solicitudes asignadas al empleado
                query = """
                    SELECT id, servicio_id, cliente_id, agencia_id, fecha_solicitud, documentos, comentarios
                    FROM solicitudes
                    WHERE empleado_id = %s and estado =%s
                """
                cursor.execute(query, (empleado_id, 'Pendiente',))
                solicitudes = cursor.fetchall()
                
                if solicitudes:
                    print("Solicitudes pendientes:")
                    for solicitud in solicitudes:
                        print("")
                        id, servicio_id, cliente_id, agencia_id, fecha_solicitud, documentos, comentarios = solicitud
                        print(f"""
                            ID: {id}
                            Servicio ID: {servicio_id}
                            Cliente ID: {cliente_id}
                            Agencia ID: {agencia_id}
                            Fecha de Solicitud: {fecha_solicitud}
                            Documentos: {documentos}
                            Comentarios: {comentarios}
                        """)
                else:
                    print("No tiene solicitudes pendientes.")
            
            except Exception as e:
                print(f"Error al obtener las solicitudes: {e}")
            
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()
        



        