"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de servicios de taxis")
    print("3- Requerimiento 1 (Reporte de Información Compañías y Taxis)")
    print("4- Requerimiento 2 (Sistema de Puntos y Premios a Taxis)")
    print("5- Requerimiento 3 (Consulta del Mejor Horario en Taxi entre 2 “community areas”)")
    print("0- Salir")
    print("*******************************************")

def optionTwo():
    print("\nCargando información de los servicios de taxis ....")
    controller.loadTrips(cont)
    
   
def optionThree():
    ene = int(input("Digite el número para el top de compañías ordenada por la cantidad de taxis afiliados\n"))
    eme = int(input("Digite el número para el top de compañías que más servicios prestaron\n"))
    controller.totalComp(cont)
    controller.totalTaxis(cont)
    controller.topCompTaxis(cont, ene)
    controller.topServComp(cont, eme)

def optionFour():
    ene=int(input("Digite la cantidad de taxis con más puntos en una fecha que desea conocer.\n"))
    fecha1=input("Digite la fecha que desea conocer.\n")
    eme=int(input("Digite la cantidad de taxis con más puntos en un rango de fechas que desea conocer.\n"))
    diain=input("Digite la fecha de inicio del rango.\n")
    diaul=input("Digite la fecha de final del rango.\n")
    controller.obtenerDia(cont,fecha1, ene)
    controller.obtenerDias(cont, diain, diaul, eme)

def optionFive():
    print("Digite el rango horario para desplazarse en el menor tiempo entre dos Community Area (HH:MM)\n")
    hora_inicial=input("Hora inicial:\n")
    hora_final=input("Hora final:\n")
    print("Ingrese el nombre de dos Community Areas\n")
    com1=str(input("Primer Community Area:\n"))
    com2=str(input("Segunda Community Area:\n"))
    controller.communityArea(cont, com1,com2, hora_inicial,hora_final)
    
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)