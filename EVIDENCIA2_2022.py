from collections import namedtuple
import datetime
import csv
import pandas as pd
import random

Cliente = namedtuple("Cliente", "nombre")
Sala = namedtuple("Sala", "nombre cupo")
Evento = namedtuple("Evento", "folio nombre_evento clave_cliente")
Clave_Evento = namedtuple("Clave_Evento","fecha clave_sala turno")
lista_turnos = {"M":"Matutino","V":"Vespertino","N":"Nocturno"}

lista_clientes = {}
lista_salas = {}
reservaciones = {}

try:
    with open("respaldo.csv", "r", newline="") as archivo: 
        lector = csv.reader(archivo)
        next(lector)
        for folio, fecha, nombre_evento, cliente, sala, turno in lector:
            reservaciones[Clave_Evento(datetime.datetime.strptime(fecha, "%Y-%m-%d").date(),int(sala),turno)] = Evento(int(folio),nombre_evento,int(cliente))
    
    with open("salas.csv", "r", newline="") as archivo: 
        lector = csv.reader(archivo)
        next(lector)
        for clave_sala, nombre_sala, cupo in lector:
            lista_salas[int(clave_sala)] = Sala(nombre_sala, int(cupo))
            
    with open("clientes.csv", "r", newline="") as archivo: 
        lector = csv.reader(archivo)
        next(lector)
        for clave_cliente, nombre_cliente, in lector:
            lista_clientes[int(clave_cliente)] = Cliente(nombre_cliente)

except Exception:
    print("No se encontró ningun respaldo. Se tomará como primer inicio del programa.\n")
else: 
    print("Se encontro un respaldo, cargando...\n")
    
while True:
    print("- " * 40)
    print(" Renta de Espacios de Coworking ".center(80, " "))
    print("Menú principal\n".center(80, " "))
    print("1. Reservaciones.")
    print("2. Reportes.")
    print("3. Registrar una Sala.")
    print("4. Registrar un Cliente.")
    print("\n0. Salir\n")
    print(" -" * 40)
    menu_op = int(input("Ingresa el número con la opción: "))

    if menu_op == 1:
        while True:
            print(f'\n{" Reservaciones ".center(80, "_")}\n')
            print("1. Registrar nueva reservación.")
            print("2. Modificar descripción de una reservación.")
            print("3. Consultar Disponibilidad de salas para una fecha")
            print("\n0. Menú Principal\n")
            print(" -" * 40)
            submenu_op = int(input("Ingresa el número con la opción: "))

            if submenu_op == 1:
                print(" -" * 40)
                print(f'\n{"---- Registrar nueva reservación ----".center(80, " ")}\n')
            
                print("***** Para realizar la reservacion se debe autenticar el cliente ****")
                print("\n0. Regresar\n")
                while True:
                    buscar_cliente = int(input("Ingrese la Clave del Cliente: "))
                    if buscar_cliente in lista_clientes.keys():
                        fecha = input("Fecha a reservar (DD/MM/YYYY): ")
                        fecha_reserva = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
                        fecha_limite_reserva = fecha_reserva - datetime.timedelta(days=+2)
                        
                        if datetime.date.today() <= fecha_limite_reserva:                
                            print(f'\n{"_" * 41}')
                            print(f"Cliente: {lista_clientes[buscar_cliente].nombre}")
                            print(f"Fecha a reservar: {fecha_reserva}\n")
                            print(f'{"Clave":<5} | {"Nombre de la Sala":<20} | {"Cupo":<8} |')
                            
                            if lista_salas == {}:
                                print("No existen salas registradas")
                                    
                            else:
                                print("-" * 41)
                                salas_ocupadas = {}
                                turnos_ocupados = []
                                
                                for e in reservaciones.keys():
                                    if fecha_reserva == e.fecha:
                                        if e.clave_sala not in salas_ocupadas.keys():
                                            turnos_ocupados = []
                                            turnos_ocupados.append(e.turno)
                                            salas_ocupadas[e.clave_sala] = turnos_ocupados
                                        else:
                                            salas_ocupadas[e.clave_sala].append(e.turno)
                                
                                for sala in lista_salas:
                                    if sala in salas_ocupadas.keys():
                                        if len(salas_ocupadas[sala]) < 3:
                                            print(f'{sala:<5} | {lista_salas[sala].nombre:<20} | {lista_salas[sala].cupo:<8} |')
                                    else:
                                        print(f'{sala:<5} | {lista_salas[sala].nombre:<20} | {lista_salas[sala].cupo:<8} |')
                                
                                sala_escoger = int(input("\nIngrese la CLAVE de la sala a escoger: ")) 
                                
                                print(f'\n{" Turnos Disponibles ".center(80, "_")}\n')
                                for turno in lista_turnos:
                                    if sala_escoger in salas_ocupadas.keys():
                                        if lista_turnos[turno] not in salas_ocupadas[sala_escoger]:
                                            print(f'{turno} - {lista_turnos[turno]}')
                                    else:
                                        print(f'{turno} - {lista_turnos[turno]}')
                                while True:  
                                    turno = input("\nTeclee la letra del turno a elegir: ").upper()
                                    if sala_escoger in salas_ocupadas.keys():
                                        if lista_turnos[turno] in salas_ocupadas[sala_escoger]:
                                            print("\n *** El Turno escogido ya esta ocupado, Porfavor escoja otro ***\n")
                                        else:
                                            break
                                    else:
                                        break

                                nombre_evento = input("Nombre del Evento: ")
                                folio = random.randint(10000,20000)
                                reservaciones[Clave_Evento(fecha_reserva,sala_escoger,lista_turnos[turno])] = Evento(folio,nombre_evento,buscar_cliente)
                                print("*"*80)
                                print("\nLa reservación se realizó con exito!\n")
                                print(f"--- Folio de Reservación: {folio}")
                                input("\nEnter para continuar\n")
                                break
                                
                        else:
                            print("\nERROR. La reservación de una sala se debe realizar al menos con 2 días de anticipación\n")
                    elif buscar_cliente == 0:
                        break
                    else: 
                        print("\n***** La clave asociada con el cliente NO se encuentra ***** | Por favor ingrese otra clave\n")
            
            if submenu_op == 2:
                while True:
                    print("- " * 41)
                    print(f'\n{"---- Modificar descripción de una reservacion ----".center(80, " ")}\n')
                    print("0. Regresar\n")
                    folio_consulta = int(input("Ingrese el folio de la reservacion: "))
                    if folio_consulta == 0:
                        break
                    else:
                        print("-" * 80)
                        for evento in reservaciones.keys():
                            if folio_consulta == reservaciones[evento].folio:
                                print(f'\nNombre del Evento: {reservaciones[evento].nombre_evento}\n')
                                nuevo_nombre = input("Nuevo nombre del evento: ")
                                n_clave_cliente = reservaciones[evento].clave_cliente
                                del reservaciones[evento]
                                reservaciones[Clave_Evento(evento.fecha,evento.clave_sala,evento.turno)] = Evento(folio_consulta,nuevo_nombre,n_clave_cliente)
                                print("\nCambios Efectuados con Exito!\n")
                                break
                        else:
                            print("No existe ninguna reservacion con ese Folio")

            if submenu_op == 3:
                print("- " * 41)
                print(f'\n{"---- Consultar Disponibilidad Salas por fecha ----".center(80, " ")}\n')
                print("0. Regresar\n")
                while True:
                    fecha_str = input("\nIngrese la fecha: ")
                    if fecha_str == '0':
                        break
                    else:
                        consultar_fecha = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
                        
                        if lista_salas == {}:
                            print("No existen salas registradas")
                                
                        else:
                            print("_" * 43)
                            print(f"\nSalas Disponibles para renta el {consultar_fecha}\n")
                            lista_reservas = list(reservaciones.keys())
                            print(f'{"Clave".center(5," "):<5} | {"SALA".center(20," "):<20} | {"TURNO".center(10," "):<10} |')
                            print("-" * 43)
                            salas_ocupadas = {}
                            for e in reservaciones.keys():
                                if consultar_fecha == e.fecha:
                                    if e.clave_sala not in salas_ocupadas.keys():
                                        turnos_ocupados = []
                                        turnos_ocupados.append(e.turno)
                                        salas_ocupadas[e.clave_sala] = turnos_ocupados
                                    else:
                                        salas_ocupadas[e.clave_sala].append(e.turno)
                            
                            for sala in lista_salas:
                                for turno in lista_turnos:
                                    if sala in salas_ocupadas.keys():
                                        if lista_turnos[turno] not in salas_ocupadas[sala]:
                                            print(f'{sala:<5} | {lista_salas[sala].nombre:<20} | {lista_turnos[turno]:<10} |')
                                    else:
                                        print(f'{sala:<5} | {lista_salas[sala].nombre:<20} | {lista_turnos[turno]:<10} |')
                            fecha_str = input("\n¿Consultar otra fecha? (1 - Si 0 - No): ")
                            if fecha_str == '0': break

                                    
            if submenu_op == 0:
                break
                
        
    elif menu_op == 2:
        print(f'\n{" Reportes ".center(80, "-")}\n')
        print("1. Reporte de reservaciones para una fecha.")
        print("2. Exportar reporte tabular (Excel).")
        print("\n0. Regresar\n")
        print(" -" * 40)
        submenu_op = int(input("Ingresa el número con la opción: \n"))

        
        if submenu_op == 1:
            print(" -" * 40)
            print(f'\n{" Reporte de Reservaciones para una fecha ".center(80, "-")}\n')
            
            fecha_str = input("Ingrese la fecha: ")
            consultar_fecha = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
            lista_reservas = list(reservaciones.keys())
            
            print(f"\n                 --- Reporte de Reservaciones para el día {consultar_fecha} ---       \n")
            print(f'{"Folio".center(5," ")} | {"Sala".center(10," ")} | {"Cliente".center(20," ")} | {"Evento".center(30," ")} | {"Turno".center(10," ")} |')
            print("-" * 90)
            for clave in lista_reservas:
                if consultar_fecha == clave.fecha:
                    for evento in [reservaciones[clave]]:
                        print(f'{evento.folio} | {lista_salas[clave.clave_sala].nombre:<10} | {lista_clientes[evento.clave_cliente].nombre:<20} | {evento.nombre_evento:<30} | {clave.turno:<10} |')
                    
            input("\nEnter para continuar\n")
            
        if submenu_op == 2:
            folios = []
            fechas = []
            salas = []
            clientes = []
            eventos = []
            turnos = []
            lista_reservas = list(reservaciones.keys())
            for clave in lista_reservas:
                for evento in [reservaciones[clave]]:
                    folios.append(evento.folio)
                    fechas.append(clave.fecha)
                    salas.append(lista_salas[clave.clave_sala].nombre)
                    clientes.append(lista_clientes[evento.clave_cliente].nombre)
                    eventos.append(evento.nombre_evento)
                    turnos.append(clave.turno)
            else:        
                e = {"FOLIO":folios,"FECHA":fechas ,"SALA":salas, "CLIENTE":clientes, "EVENTO":eventos, "TURNO":turnos}        
                df = pd.DataFrame(e)
                try:
                    df.to_xlsx('Reporte_Reservaciones.xlsx',index=False)
                except Exception:
                    print(" *** ERROR *** Ocurrio un problema para exportar el archivo")
                    input("\nEnter para continuar\n")
                else:
                    print(f"Se ha generado un archivo XLSX en la ruta actual")
        
    elif menu_op == 3:
        print(f'\n{" Registrar una Sala ".center(80, "-")}\n')
        while True:
            nombre_sala = input("Ingrese el nombre de la Sala: ")
            if len(nombre_sala) == 0 and nombre_sala.strip() == '':
                print("Este campo no puede omitirse\n")
            else:
                break
        while True:
            cupo = input("Ingrese el cupo total para la Sala: ")
            if len(cupo) == 0 and cupo.strip() == '':
                print("El cupo no puede estar vacio\n")
            elif int(cupo) <= 0:
                print("El numero debe ser mayor a 0\n")
            else:
                break

        clave_sala = random.randint(100,200)
        
        while clave_sala == lista_salas.keys():
            clave_sala = random.randint(100,200)

        lista_salas[clave_sala] = Sala(nombre_sala, cupo)
        print("-" * 80)
        print("\nSala registrada con exito!\n")
        print(f"--- Clave de la Sala: {clave_sala}")
        input("\nEnter para continuar\n")
    
    
    elif menu_op == 4:
        print(f'\n{" Registrar un Cliente ".center(80, "-")}\n')
        while True:
            nombre_cliente = input("Ingrese el nombre del Cliente: ")
            if len(nombre_cliente) == 0 and nombre_cliente.strip() == '':
                print("Este campo no puede omitirse\n")
            else:
                break
            
        clave_cliente = random.randint(100,200)
        
        while clave_cliente == lista_clientes.keys():
            clave_cliente = random.randint(100,200)

        lista_clientes[clave_cliente] = Cliente(nombre_cliente)
        print("-" * 80)
        print("\nCliente registrado con exito!\n")
        print(f"--- Clave del Cliente: {clave_cliente}")
        input("\nEnter para continuar\n")
    
    
    elif menu_op == 0:
        with open("respaldo.csv", "w", newline="") as archivo:
            grabador = csv.writer(archivo)
            grabador.writerow(("Folio", "Fecha_reserva", "Nombre_evento", "Cliente", "Sala", "Turno")) #Encabezado
            for clave, evento in reservaciones.items():
                grabador.writerow((evento.folio, clave.fecha, evento.nombre_evento, evento.clave_cliente, clave.clave_sala, clave.turno))
            
        with open("salas.csv", "w", newline="") as archivo:
            grabador = csv.writer(archivo)
            grabador.writerow(("Clave", "Nombre_sala", "Cupo"))
            for clave, sala in lista_salas.items():
                grabador.writerow((clave,sala.nombre,sala.cupo))
                    
        
        with open("clientes.csv", "w", newline="") as archivo:
            grabador = csv.writer(archivo)
            grabador.writerow(("Clave", "Nombre_cliente"))
            for clave, cliente in lista_clientes.items():
                grabador.writerow((clave,cliente.nombre))
        
        break