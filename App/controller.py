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

import config as cf
from App import model
from DISClib.ADT import map as m
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def totalComp(analyzer):
    print(str(model.numTotalComp(analyzer)))

def totalTaxis(analyzer):
    print(str(model.numTotalTaxis(analyzer)))

def topCompTaxis(analyzer, cuantos):
    lista = model.topCompTaxis(analyzer)
     i=0
    while i<cuantos:
        elemento = lt.getElement(lista, i)
        i+=1
        print(str(i) + ". " + str(elemento['name']) + " con " + str(m.size(elemento['taxis'])) + " puntos")

def topServComp(analyzer, cuantos):
    lista = model.topServComp(analyzer)
     i=0
    while i<cuantos:
        elemento = lt.getElement(lista, i)
        i+=1
        print(str(i) + ". " + str(elemento['name']) + " con " + str(elemento['cuantosviajes']) + " puntos")

def obtenerDia(analyzer, dia, cuantos):
    din = datetime.datetime.strptime(dia, '%Y-%m-%d')
    lista = model.obtenerDia(analyzer, din )
    i=0
    while i<cuantos:
        elemento = lt.getElement(lista, i)
        i+=1
        print(str(i) + ". " + str(elemento['taxiid']) + " con " + str(elemento['puntos']) + " puntos")

def obtenerDias(analyzer, diain, diaul, cuantos):
    din = datetime.datetime.strptime(diain, '%Y-%m-%d')
    dend = datetime.datetime.strptime(diaul, '%Y-%m-%d')
    lista = model.obtenerDias(analyzer, din, dend )
    i=0
    while i<cuantos:
        elemento = lt.getElement(lista, i)
        i+=1
        print(str(i) + ". " + str(elemento['taxiid']) + " con " + str(elemento['puntos']) + " puntos")

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________