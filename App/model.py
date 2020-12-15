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
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
import datetime
from datetime import date
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
    
    if not gr.containsVertex(analyzer['viajes'], stopin):
        gr.insertVertex(analyzer['viajes'], stopin)
    if not gr.containsVertex(analyzer['viajes'], stopfin):
        gr.insertVertex(analyzer['viajes'], stopfin)

    edge = gr.getEdge(analyzer['viajes'], stopin, stopfin)
    if edge is None :
        gr.addEdge(analyzer['viajes'], stopfin, stopfin, duracion)

    return analyzer

def taxi(analyzer, service):
    entry = m.get(analyzer['taxis'], service["taxi_id"])
    tiempo=0.0
    if service["trip_seconds"] !='':
        tiempo = float(service["trip_seconds"]) 
    if entry is None:
        infoService ={"cuantosViajes":1 ,"id" : service["taxi_id"], "tiempoUso": tiempo , 'distancia':float(service['trip_miles']),"viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips)}
        lt.addLast(infoService["viajes"], service)
        m.put(analyzer['taxis'], service["taxi_id"], infoService)
    else:
        infoService = entry['value']
        if infoService["id"]==service["taxi_id"]:
            infoService["cuantosViajes"]+=1
            infoService["tiempoUso"]+= tiempo
            lt.addLast(infoService["viajes"],service)

def addcompañia(analyzer, compañia, service):
    entry = m.get(analyzer['empresas'], compañia)
    if entry is None:
        infoCompany = {'name': compañia, 'cuantosviajes':1, 'cuantosTaxis': 0, 'taxis' : m.newMap(numelements=2000, maptype='PROBING', comparefunction=compareTaxis) }
        m.put(analyzer['empresas'], compañia, infoCompany)    
    else:
        infoCompany = entry['value']

    taxi = m.get(infoCompany['taxis'], service['taxi_id'])
    if taxi is None:
        infotaxi = {'taxi_id':service['taxi_id'] ,'cuantosServicios':1 }
        infoCompany['cuantosTaxis']+=1
        m.put(infoCompany['taxis'], service['taxi_id'], infotaxi)
    else :
        infotaxi = taxi['value']
        infotaxi['cuantosServicios']+=1
        

def uptadeHour(analyzer,service):
    date = service['trip_start_timestamp']
    serviceDate = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
    formato=":"
    if serviceDate.minute>=30:
        formato=str(serviceDate.hour)+":30"
    elif serviceDate.minute<30:
        formato=str(serviceDate.hour)+":00"
   
    entry = om.get(analyzer['hora'], formato)

    if entry is None:
        hour_entry = {'hour': formato, 'service': lt.newList('SINGLE_LINKED', compareHours)}
        om.put(analyzer['hora'] ,formato, hour_entry)  
    else:
        hour_entry = me.getValue(entry)
    
    lt.addLast(hour_entry['service'], service)
    hour_entry['hour']= format
    return analyzer

def uptadeDate(analyzer,service):
    date = service['trip_start_timestamp']
    serviceDate = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
    entry = om.get(analyzer['fechas'], serviceDate.date())

    if entry is None:
        date_entry ={'service': lt.newList('SINGLE_LINKED', compareDates) , 'taxi': m.newMap(numelements=2000,maptype='PROBING',comparefunction=compareTaxis)}
        om.put(analyzer['fechas'] ,serviceDate.date(), date_entry)  
    else:
        date_entry = me.getValue(entry)
    lt.addLast(date_entry['service'], service)

    taxi = m.get(date_entry['taxi'], service['taxi_id'])
    dinero=0.0
    millas=0.0
    if service['trip_miles'] != '':
        millas = float(service['trip_miles'])
    if service['trip_total'] != '':
        dinero = float(service['trip_total'])
    if taxi is None:
        infotaxi = {'taxiid':service['taxi_id'] ,'cuantosServicios':1 , 'cuantasMillas': millas,'cuantoDinero':dinero,'puntos':0.0, 'viajes': lt.newList('SINGLE_LINKED', compareDates) }
        if infotaxi['cuantoDinero']!=0:
            infotaxi['puntos']=((infotaxi['cuantasMillas']/infotaxi['cuantoDinero'])*infotaxi['cuantosServicios'])
        lt.addLast(infotaxi['viajes'], service)
        m.put(date_entry['taxi'], service['taxi_id'], infotaxi)
    else :
        infotaxi = taxi['value']
        infotaxi['cuantosServicios']+=1
        infotaxi['cuantasMillas']+= millas
        infotaxi['cuantoDinero']+= dinero
        if infotaxi['cuantoDinero']!=0:
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
    ms.mergesort(lista, comparaTaxiRank)
    #ist.insertionSort(lista, comparaTaxiRank)
    return lista
def topServComp(analyzer):
    lista = converirLista(analyzer['empresas'])
    ms.mergesort(lista, comparaServicios)
    #ist.insertionSort(lista, comparaServicios)
    return lista
def obtenerDia(analyzer, dia):
    diain = om.get(analyzer['fechas'], dia)['value']['taxi']
    lista = converirLista(diain)
    ms.mergesort(lista, comparaPuntos)
    return lista
def obtenerDias(analyzer, diain, diaul):
    lista = lt.newList("ARRAY_LIST", cmpfunction=compareTaxis)
    llaves = om.keys(analyzer['fechas'], diain,diaul)
    iterator= it.newIterator(llaves)
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['fechas'],info)['value']['taxi']
        converirListas(valor, lista)
    ms.mergesort(lista, comparaPuntos)
    return lista
    
def communityArea(analyzer, origen, destino, timein, timefin):
    graph = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=10000, comparefunction=compareTrips)
    llaves = om.keys(analyzer['hora'],timein, timefin)
    iterator= it.newIterator(llaves)
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['hora'],info)['value']['service']
        ite = it.newIterator(valor)
        while (it.hasNext(ite)):
            inf= it.next(ite)
            inicio= inf['pickup_community_area']
            final= inf['dropoff_community_area']
            duracion = inf['trip_seconds']
            if not gr.containsVertex(graph, inicio):
                gr.insertVertex(graph, inicio)
            if not gr.containsVertex(graph, final):
                gr.insertVertex(graph, final)
            edge = gr.getEdge(graph, inicio, final)
            if edge is None:
                gr.addEdge(graph, inicio, final, duracion)
    
    if gr.containsVertex(graph, stopin) and gr.containsVertex(graph, final):
        lista1 = lt.newList("ARRAY_LIST")
        adyacentes = gr.adjacents(graph, origen)
        analyzer['components'] = scc.KosarajuSCC(graph)
        for h in range (adyacentes['size']):
            adyacente= lt.getElement(adyacentes,h)
            fcc = sameCC(graph, estacion, adyacente)
            if fcc:
                tiempo=0
                analyzer['paths'] = dfs.DepthFirstSearch(graph, adyacente)
                caminos = dfs.pathTo(analyzer["paths"], estacion)
                primero= caminos['first']
                siguiente = primero['next']
                for i in range(caminos['size']-1):
                    infoin = primero['info']
                    if siguiente is not None:
                        infoul = siguiente['info']
                        arco = gr.getEdge(graph, infoin, infoul)
                        if arco is not None:
                            tiempo += float(arco["weight"])
                    primero = primero['next']
                    siguiente = siguiente['next']
                suma = float(caminos['size'])*1200
                tiempo+=suma
                lt.addLast(caminos,tiempo)
                lt.addLast(lista1, caminos)

        tiempo1=100000000.0
        rta={}
        listafinal= lt.newList("ARRAY_LIST")
        if lista1 is not None:
            tmi = int(tiempoin)*60
            tmf = int(tiempofin)*60
            while (not stack.isEmpty(lista1)):
                parada = stack.pop(lista1)
                if float(parada['last']['info']) > tiempo1: 
                    tiempo1= float(parada['last']['info'])
                    rta = parada
        return rta

def sameCC(analyzer, station1, station2):
    vert1 = gr.containsVertex(analyzer, station1)
    vert2 = gr.containsVertex(analyzer, station2)
    if vert1 is False and vert2 is False:
        return "0"
    elif vert1 is False:
        return "1"
    elif vert2 is False:
        return "2"
    else:
        return scc.stronglyConnected(analyzer['components'], station1, station2)



# ==============================
# Funciones Helper
# ==============================

def converirLista(map):
    lista = lt.newList("ARRAY_LIST")
    llaves = m.keySet(map)
    ite = it.newIterator(llaves)
    while(it.hasNext(ite)):
        info=it.next(ite)
        actual = m.get(map,info)['value']
        lt.addLast(lista, actual)
    return lista

def converirListas(map, lista):
    llaves = m.keySet(map)
    ite = it.newIterator(llaves)
    while(it.hasNext(ite)):
        info=it.next(ite)
        actual = m.get(map,info)['value']
        lt.addLast(lista, actual)
    return lista

# ==============================
# Funciones de Comparacion
# ==============================
def comparaServicios(element1, element2):
    if float(element1['cuantosviajes']) > float(element2['cuantosviajes']) and element2 is not None:
        return True
    return False

def comparaTaxiRank(element1, element2):
    if element1 is not None and element2 is not None:
        if float(element1['cuantosTaxis']) > float(element2['cuantosTaxis']) :
            return True
    return False

def comparaPuntos(element1, element2):
    if float(element1['puntos']) > float(element2['puntos']) and element2 is not None:
        return True
    return False

def compareTrips(trip1, trip2):
    if (trip1 == trip2['key']):
        return 0
    elif (trip1 > trip2['key']):
        return 1
    else:
        return -1

def compareTaxis(trip1, trip2):
    if (trip1 == trip2['key']):
        return 0
    elif (trip1 > trip2['key']):
        return 1
    else:
        return -1

def compareCompany(trip1, trip2):
    if (trip1 == trip2['key']):
        return 0
    elif (trip1 > trip2['key']):
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