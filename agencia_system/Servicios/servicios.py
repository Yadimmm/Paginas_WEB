# CLASES PARA AGENCIAS Y SUS SERVICIOS
#Paquete 'Servicios'
#servicios.py

from conexionBD import obtener_conexion
from funciones import *
from datetime import datetime, timedelta #es que porque pones agregar cita aqui mana
#timedelta es una clase de modulo datetime y representa una duracion o diferencias entre fechas y horas

class Agencias:
    def __init__(self, id, nombre, direccion, telefono, descripcion):
        self.__id = id
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.descripcion = descripcion

    # GETTER Y SETTER
    def getAgencia(self):
        return self.__id

    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre = nombre

    def getDireccion(self):
        return self.__direccion

    def setDireccion(self, direccion):
        self.__direccion = direccion

    def getTel(self):
        return self.__telefono

    def setTel(self, telefono):
        self.__telefono = telefono


    # FUNCIONES DE LA AGENCIA
    def mostrar_detalles(self):
        # Código para mostrar detalles de las agencias disponibles
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM agencias")
            for (id, nombre, direccion, telefono, descripcion) in cursor: #iterar para que se vea bonito
                print(f"ID: {id}\n Nombre: {nombre} \n Dirección: {direccion} \n Teléfono: {telefono} \n ||||||| {descripcion}")
                print(" ")
            cursor.close()
            conexion.close()
        else:
            print("No se pudo establecer la conexión a la base de datos.")


            


    
      


class Citas:
    def __init__(self, id, fecha, id_cliente, id_empleado, id_solicitud, estado):
        self.__id = id
        self.__id_cliente = id_cliente
        self.__id_cliente = id_cliente
        self.__id_empleado = id_empleado
        self.__id_solicitud = id_solicitud
        self.estado=estado

    # METODOS GET PARA ACCEDER A ELLOS
    @property
    def id_cita(self):
        return self.__id

    @property
    def id_cliente(self):
        return self.__id_cliente

    @property
    def id_empleado(self):
        return self.__id_empleado

    @property
    def id_servicio(self):
        return self.__id_servicio

    # FUNCIONES DE LAS CITAS
    def confirmar(self, id_cita):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            # Verificar si la cita existe
            cursor.execute("SELECT COUNT(*) FROM citas WHERE id = %s", (id_cita,))
            resultado = cursor.fetchone() #guardar el resultado en una tupla

            if resultado[0] == 0:
                print(f"Lo sentimos... esta cita no se ha programado.")
            else:
                respuesta = input("¿Seguro que confirmará esta cita? (si/no): ").upper()
                if respuesta in ['SI', 'YES', 'S']:  # Condición mejorada
                    cursor.execute(
                        "UPDATE citas SET estado = %s WHERE id = %s", 
                        ('Confirmada', id_cita)
                    )
                    conexion.commit()
                    limpiarPantalla()
                    print(f"Cita con ID {id_cita} confirmada.")
                    
                    # Obtener y mostrar la fecha de la cita
                    cursor.execute("SELECT fecha_cita FROM citas WHERE id = %s", (id_cita,))
                    fecha = cursor.fetchone()
                    
                    if fecha:
                        fecha_formateada = fecha[0]  # Extrae la fecha de la tupla
                        print(f"Cita confirmada para el {fecha_formateada}.")
                    else:
                        print("No se pudo recuperar la fecha de la cita.")
                else:
                    limpiarPantalla()
                    print("La confirmación ha sido cancelada.")
        except Exception as e:
            limpiarPantalla()
            print(f"Error al confirmar la cita: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()



    def cancelar_cita(self, id_cita):
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            # Verificar si la cita existe
            cursor.execute("SELECT COUNT(*) FROM citas WHERE id = %s", (id_cita,))
            resultado = cursor.fetchone() #guardar el resultado en una tupla

            if resultado[0] == 0:
                print(f"Lo sentimos... esta cita no se ha programado.")
            else:
                respuesta = input("¿Seguro que cancelará esta cita? (si/no): ").upper() #convierte en mayusculas
                if respuesta in ['SI', 'YES', 'S']:  # Condición mejorada
                    cursor.execute(
                        "UPDATE citas SET estado = %s WHERE id = %s", 
                        ('Cancelada', id_cita)
                    )
                    conexion.commit()
                    print(f"Cita con ID {id_cita} cancelada.")
                    
                elif respuesta in ['NO', 'N', 'NOPE']: #si pone un NO
                    print("La operación para cancelar no fue ejecutada.") 
        except Exception as e:
            print(f"Error al cancelar la cita: {e}")    
        finally:
            if conexion:
                cursor.close()
                conexion.close()



    def mostrar_citas(self, id_cliente):
        # Conectar a la base de datos
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            # Consultar todas las citas del cliente
            cursor.execute("""
                SELECT id, cliente_id, solicitud_id, empleado_id, fecha_cita, estado
                FROM citas
                WHERE cliente_id = %s
            """, (id_cliente,))
            
            resultados = cursor.fetchall()  # Obtener todos los resultados en una tupla
            
            if resultados:
                print(f"Citas para usted:")
                for resultado in resultados:  # Iterar para imprimir
                    id_cita, cliente_id, id_solicitud, id_empleado, fecha, estado = resultado
                    # Imprimir los detalles de cada cita
                    print(f"\nID de su cita: {id_cita}")
                    print(f"\nUsuario solicitante: {cliente_id}")
                    print(f"ID del Profesional: {id_empleado}")
                    print(f"ID de la solicitud: {id_solicitud}")
                    print(f"Estado: {estado}")
                    print(f"Fecha: {fecha}")
            else:
                print("No se encontraron citas para usted")
            
        except Exception as e:
            print(f"Error al mostrar las citas: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()



class Servicios:
    def __init__(self, id_servicio, nombre, descripcion, empleado_id, agencia_id):
        self.__id_servicio = id_servicio
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__empleado_id = empleado_id
        self.__agencia_id = agencia_id

    # GET Y SET
    def getId(self):
        return self.__empleado_id

    def getId_empleado(self):
        return self.__agencia_id

    def getId_agencia(self):
        return self.__id_servicio

    def getIdVeterinaria(self):
        return self.__id_veterinaria

    def setId(self, id_servicio):
        self.__id_servicio = id_servicio

    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre = nombre

    def getDescripcion(self):
        return self.__descripcion

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion


    # FUNCIONES PARA LOS SERVICIOS
    def mostrar_servicios(self):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM servicios ")
            for (id_servicio, nombre, descripcion, empleado_id, agencia_id) in cursor: #iterar para que se vea bonito
                print("")
                print(f"\nID: {id_servicio}\n Nombre: {nombre} \n Descripcion: {descripcion} \n Profesional a cargo: {empleado_id}\n Agencia: {agencia_id} ")
            cursor.close()
            conexion.close()
        else:
            print("No se pudo establecer la conexión a la base de datos.")




class Solicitudes:
    def __init__(self, id, id_cliente, id_servicio, fecha_solicitud, estado, documentos, comentarios):
        self.id = id
        self.id_cliente = id_cliente
        self.id_servicio = id_servicio
        self.fecha_solicitud = fecha_solicitud
        self.estado = estado
        self.documentos = documentos
        self.comentarios = comentarios

    #FUNCIONES PARA SOLICITUD


    @staticmethod
    def mostrar_solicitudes(id_cliente):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                # Mostrar solicitudes del cliente
                cursor.execute("SELECT id, servicio_id, fecha_solicitud, estado FROM solicitudes WHERE cliente_id = %s", (id_cliente,))
                solicitudes = cursor.fetchall()
                
                if not solicitudes:
                    print("No has hecho solicitudes...¡Te invitamos a hacer una!")
                    return
                
                # Mostrar solicitudes para que el cliente elija
                print("Tus solicitudes:")
                print("") #pa que se vea astetik
                for solicitud in solicitudes:
                    print(f"ID: {solicitud[0]}\n Servicio ID: {solicitud[1]}\n Fecha de Solicitud: {solicitud[2]}\n Estado: {solicitud[3]}")

            except Error as e:
                print(f"Error al consultar las solicitudes: {e}")
                
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()
 
    