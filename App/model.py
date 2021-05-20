"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """Inicializa el catálogo, es decir el grafo

    """

    catalog = {"LandingPoints": mp.newMap(numelements=14000,
                                            maptype='CHAINING',
                                            comparefunction=compareLandingPoints),
                "Connections": gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=14000,
                                            comparefunction=compareLandingPoints),
                "Paths": mp.newMap(numelements=14000,
                                            maptype='CHAINING',
                                            comparefunction=compareLandingPoints),
                "Countries": mp.newMap(numelements=14000,
                                            maptype='CHAINING',
                                            comparefunction=compareLandingPoints)}

    return catalog

# Funciones para agregar informacion al catalogo

def addConnection(catalog, connection):
    
    origin = int(connection['\ufefforigin'])
    destination = int(connection['destination'])
    lenght = formatLength(connection['cable_length'])
      
    addNode(catalog, origin)
    addNode(catalog, destination)
    addEdge(catalog, origin, destination, lenght)
    addPath(catalog, origin, destination, connection)
    
    return catalog


def addCountries(catalog, country):

    addCountry(catalog, country)
    return catalog



def addLandingPoints(catalog, landingpoint):

    addLandingPoint(catalog, landingpoint)

    return catalog



# Funciones para creacion de datos

def addNode(catalog, landPointId):
    """revisa si ya hay un vertex en connectios con el Id que entra por parametro, y si no está
    lo agrega"""

    if not gr.containsVertex(catalog["Connections"], landPointId):
        gr.insertVertex(catalog["Connections"], landPointId)

    return catalog


def addEdge(catalog, origin, destination, length):
    """revisa si hay un arco entre el origin y el destination y si no lo encuentra lo añade"""

    ofGlory = gr.getEdge(catalog["Connections"], origin, destination)

    if ofGlory is None:
        gr.addEdge(catalog["Connections"], origin, destination, length)

    return catalog


def addPath(catalog, origin, destination, connection):
    
    path = str(origin)+"-"+str(destination)

    entry = mp.get(catalog["Paths"], path)

    if entry is None:
        novaEntry = {"origin": origin,
                     "destination": destination, 
                     "cableName": connection["cable_name"], 
                     "cableId": connection["cable_id"],
                     "cableLength": connection["cable_length"],
                     "owners": connection["owners"], 
                     "capacity": float(connection["capacityTBPS"])}
        mp.put(catalog["Paths"], path, novaEntry)

    return catalog


def addCountry(catalog, country):

    nomen = country["CountryName"]

    initus = mp.get(catalog["Countries"], nomen)

    if initus is None:
        novusinit = {"name": country["CountryName"],
                     "capital": country["CapitalName"], 
                     "code": country["CountryCode"], 
                     "latitude": country["CapitalLatitude"],
                     "longitude": country["CapitalLongitude"],
                     "continent": country["ContinentName"], 
                     "population": int(country["Population"].replace(".", "")),
                     "users": int(country["Internet users"].replace(".", ""))}
        
        mp.put(catalog["Countries"], nomen, initus)
    return catalog


def addLandingPoint(catalog, landingpoint):
    
    lanid = int(landingpoint['landing_point_id'])

    inita = mp.get(catalog['LandingPoints'], lanid)

    if inita is None:
        novuminit = {"Landid": int(landingpoint["landing_point_id"]),
                     "id": landingpoint['id'],
                     "name": landingpoint["name"],
                     "latitude": landingpoint["latitude"],
                     "longitude": landingpoint["longitude"]}

        mp.put(catalog['LandingPoints'], lanid, novuminit)

    return catalog




# Funciones de consulta

def totalVertex(catalog):

    return gr.numVertices(catalog["Connections"])



def totalEdges(catalog):

    return gr.numEdges(catalog["Connections"])



# Funciones utilizadas para comparar elementos dentro de una lista

def compareLandingPoints(stop, keyValue):
    """Compara enytre dos Landing-Points"""

    key = keyValue["key"]

    if stop == key:
        return 0
    elif stop > key:
        return 1
    else:
        return -1



# Funciones de ordenamiento

def formatLength(length):

    if length == "n.a.":
        length = 0
    else:
        length = length.split(" ")
        length = float(length[0].replace(",", ""))
    
    return length