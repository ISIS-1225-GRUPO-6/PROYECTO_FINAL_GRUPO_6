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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as ist
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""
def newAnalyzer():
   
    analyzer = {'taxis': None,
                'empresas': None,
                'fechas': None,
                'hora': None,
                'viajes': None,
                'components': None,
                'paths': None
                    }

    analyzer['taxis'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareTaxis)

    analyzer['empresas'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareCompany)

    analyzer['fechas'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
                        
    analyzer['hora'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHours)

    analyzer['viajes'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10000,
                                              comparefunction=compareTrips)
    return analyzer

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo

def añadirViaje(analyzer, service):
    inicio= service['pickup_community_area']
    final= service['dropoff_community_area']
    duracion = service['trip_seconds']
    compañia = service['company']
    addGraph(analyzer,inicio,final,duracion)
    taxi(analyzer, service)
    uptadeDate(analyzer, service)
    uptadeHour(analyzer,service)
    if compañia is None:
        addcompañia(analyzer, "Independent Owner" ,service)
    else:
        addcompañia(analyzer, compañia ,service)

def addGraph(analyzer, stopin, stopfin, duracion):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['viajes'], stopin):
            gr.insertVertex(analyzer['viajes'], stopin)

        if not gr.containsVertex(analyzer['viajes'], stopfin):
            gr.insertVertex(analyzer['viajes'], stopfin)

        edge = gr.getEdge(analyzer["graph"], stopin, stopfin)
        if edge is None or edge > duracion:
            gr.addEdge(analyzer["graph"], stopfin, stopfin, duracion)

        return analyzer

def taxi(analyzer, service):
    entry = m.get(analyzer['taxis'], service["taxi_id"])
    if entry is None:

        infoService ={"cuantosViajes":1 ,"id" : service["taxi_id"], "tiempoUso": int(service["trip_seconds"]) , 'distancia':float(service['tripmiles']),"viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips)}
        lt.addLast(infoService["viajes"], service)
        m.put(analyzer['taxis'], service["taxi_id"], infoService)
    else:
        infoService = entry['value']
        if infoService["id"]==service["taxi_id"]:
            infoService["cuantosViajes"]+=1
            infoService["tiempoUso"]+= int(service["trip_seconds"])
            lt.addLast(infoService["viajes"],service)

def addcompañia(analyzer, compañia, service):
    entry = m.get(analyzer['empresas'], compañia)
    if entry in None:
        infoCompany = {'name': compañia, 'cuantosviajes':1, 'taxis' : m.newMap(numelements=2000, maptype='PROBING', comparefunction=compareTaxis) }
        m.put(analyzer['empresas'], compañia, infoCompany)    
    else:
        infoCompany = entry['value']

    taxi = m.get(infoCompany['taxis'], service['taxi_id'])
    if taxi is None:
        infotaxi = {'taxi_id':service['taxi_id'] ,'cuantosServicios':1, 'viajes': lt.newList('SINGLE_LINKED', compareTaxis) }
        lt.addLast(infotaxi['viajes'], service)
        m.put(infoCompany['taxis'], service['taxi_id'], infotaxi)
    else :
        infotaxi = taxi['value']
        infotaxi['cuantosServicios']+=1
        lt.addLast(infotaxi['viajes'], service)
    
def newHourEntry():
 
    entry = {'hour': None, 'service': None}
    entry['service'] = lt.newList('SINGLE_LINKED', compareHours)
    return entry

def newDateEntry():
 
    entry = {'service': None, 'taxi': None }
    entry['service'] = lt.newList('SINGLE_LINKED', compareDates)
    entry['taxi']= m.newMap(numelements=2000,maptype='PROBING',comparefunction=compareTaxis)
    return entry

def uptadeHour(analyzer,service):
    date = service['Start_Time']
    serviceDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    formato=":"
    if serviceDate.minute>=30:
        formato=str(serviceDate.hour)+":30"
    elif serviceDate.minute<30:
        formato=str(serviceDate.hour)+":00"
   
    entry = om.get(analyzer['hora'], formato)

    if entry is None:
        hour_entry = newHourEntry()
        om.put(analyzer['hora'] ,formato, hour_entry)  
    else:
        hour_entry = me.getValue(entry)
    
    lt.addLast(hour_entry['service'], service)
    hour_entry['hour']= format
    return analyzer

def uptadeDate(analyzer,service):
    date = service['trip_start_timestamp']
    serviceDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    entry = om.get(analyzer['fechas'], serviceDate.date())

    if entry is None:
        date_entry = newDateEntry()
        om.put(analyzer['fechas'] ,serviceDate.date(), date_entry)  
    else:
        date_entry = me.getValue(entry)
    
    lt.addLast(date_entry['service'], service)
    taxi = m.get(date_entry['taxis'], service['taxi_id'])
    millas = float(service['trip_miles'])
    dinero = float(service['trip_total'])
    if taxi is None:
        infotaxi = {'taxiid':service['taxi_id'] ,'cuantosServicios':1 , 'cuantasMillas': millas,'cuantoDinero':dinero,'puntos':0.0, 'viajes': lt.newList('SINGLE_LINKED', compareDates) }
        infotaxi['puntos']=((infotaxi['cuantasMillas']/infotaxi['cuantoDinero'])*infotaxi['cuantosServicios'])
        lt.addLast(infotaxi['viajes'], service)
        m.put(date_entry['taxis'], service['taxi_id'], infotaxi)
    else :
        infotaxi = taxi['value']
        infotaxi['cuantosServicios']+=1
        infotaxi['cuantasMillas']+= millas
        infotaxi['cuantoDinero']+= dinero
        infotaxi['puntos']=((infotaxi['cuantasMillas']/infotaxi['cuantoDinero'])*infotaxi['cuantosServicios'])
        lt.addLast(infotaxi['viajes'], service)

    return analyzer
# ==============================
# Funciones de consulta
# ==============================

def numTotalTaxis(analyzer):
    return m.size(analyzer['taxis'])
def numTotalComp(analyzer):
    return m.size(analyzer['empresas'])
def topCompTaxis(analyzer):
    lista = converirLista(analyzer['empresas'])
    ist.insertionSort(lista, comparaTaxiRank)
    return lista
def topServComp(analyzer):
    lista = converirLista(analyzer['empresas'])
    ist.insertionSort(lista, comparaServicios)
    return lista
def obtenerDia(analyzer, dia):
    diain = om.get(analyzer['fechas'], dia)['value']['taxi']
    lista = converirLista(diain)
    ist.insertionSort(lista, comparaPuntos)
    return lista
def obtenerDias(analyzer, diain, diaul):
    lista = lt.newList("ARRAY_LIST", cmpfunction=compareTaxis)
    llaves = om.keys(analyzer['fechas'], diain,diaul)
    iterator= it.newIterator(llaves)
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['fechas'],info)['value']['taxi']
        converirListas(valor, lista)
    ist.insertionSort(lista, comparaPuntos)
    return lista
    
def communityArea(analyzer, origen, destino, timein, timefin):

    llaves = om.keys(analyzer['hora'],timein, timefin)
    iterator= it.newIterator(llaves)
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['hora'],info)['value']['service']
        



# ==============================
# Funciones Helper
# ==============================

def converirLista(map):
    lista = lt.newList("ARRAY_LIST", cmpfunction=compareTaxis)
    llaves = m.keySet(map)
    ite = it.newIterator(llaves)
    while(it.hasNext(ite)):
        info=it.next(ite)
        actual = m.get(analyzer['stationsStart'],info)['value']
        lt.addLast(lista, actual)
    return lista

def converirListas(map, lista):
    llaves = m.keySet(map)
    ite = it.newIterator(llaves)
    while(it.hasNext(ite)):
        info=it.next(ite)
        actual = m.get(analyzer['stationsStart'],info)['value']
        lt.addLast(lista, actual)
    return lista

# ==============================
# Funciones de Comparacion
# ==============================
def comparaServicios(element1, element2):
    if float(element1['cuantosviajes']) > float(element2['cuantosviajes']):
        return True
    return False

def comparaTaxiRank(element1, element2):
    taxis1 = m.size(element1['taxis'])
    taxis2 = m.size(element2['taxis'])
    if int(taxis1) > int(taxis2):
        return True
    return False

def comparaPuntos(element1, element2):
    if float(element1['puntos']) > float(element2['puntos']):
        return True
    return False

def compareTrips(trip1, trip2):
    if (trip1 == trip2):
        return 0
    elif (trip1 > trip2):
        return 1
    else:
        return -1

def compareTaxis(trip1, trip2):
    if (trip1 == trip2['key']):
        return 0
    elif (trip1 > trip2):
        return 1
    else:
        return -1

def compareCompany(trip1, trip2):
    if (trip1 == trip2['key']):
        return 0
    elif (trip1 > trip2):
        return 1
    else:
        return -1

def compareDates(date1, date2):

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else: 
        return -1

def compareHours(hour1, hour2):
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2) :
        return 1
    else:
        return -1