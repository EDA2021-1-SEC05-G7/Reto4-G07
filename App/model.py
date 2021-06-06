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
from DISClib.ADT import graph as gr
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

def newCatalog():
    """
    Create a new catalog with information provided
    """

    catalog = {
        "LandingPoints": mp.newMap(numelements=14000, maptype='CHAINING'),
        "Connections": mp.newMap(numelements=14000, maptype='CHAINING'),
        "Countries": mp.newMap(numelements=14000, maptype='CHAINING'),
        "Graph": gr.newGraph(datastructure='ADJ_LIST', directed=True, size=14000),
        "LandingPointsByName": mp.newMap(numelements=25000, maptype='PROBING')
    }

    return catalog

# Add info to catalog
def addConnection(catalog, connection):
    """
    Add a connection and update graph info
    """

    origin = int(connection['\ufefforigin'].strip())
    destination = int(connection['destination'].strip())
    length = formatLength(connection['cable_length'].strip())

    __addNode(catalog, origin)
    __addNode(catalog, destination)
    __addEdge(catalog, origin, destination, length)

    connection_instance = {
        "origin": origin,
        "destination": destination,
        "cable_name": connection["cable_name"].strip(),
        "cable_id": connection["cable_id"].strip(),
        "cable_length": length,
        "cable_rfs": connection["cable_rfs"].strip(),
        "owners": connection["owners"].strip(),
        "capacityTBPS": connection["capacityTBPS"].strip()
    }

    mp.put(catalog["Connections"], str(origin)+"-"+str(destination), connection_instance)


def addCountry(catalog, country):
    """
    add a new country into the catalog
    """

    country_instance = {
        "CountryName": country["CountryName"].strip(),
        "CapitalName": country["CapitalName"].strip(),
        "CapitalLatitude": float(country["CapitalLatitude"].strip()),
        "CapitalLongitude": float(country["CapitalLongitude"].strip()),
        "CountryCode": country["CountryCode"].strip(),
        "ContinentName": country["ContinentName"].strip(),
        "Population": country["Population"].strip(),
        "InternetUsers": country["Internet users"].strip()
    }

    mp.put(catalog["Countries"], country["CountryName"].strip(), country_instance)


def addLandingPoint(catalog, landingpoint):
    """
    Add a new landing point to catalog
    """

    landingpoint_instance = {
        "landing_point_id": int(landingpoint["landing_point_id"].strip()),
        "id": landingpoint["id"].strip(),
        "name": landingpoint["name"],
        "latitude": float(landingpoint["latitude"].strip()),
        "longitude": float(landingpoint["longitude"].strip())
    }

    mp.put(catalog["LandingPoints"], int(landingpoint["landing_point_id"].strip()), landingpoint_instance)
    mp.put(catalog["LandingPointsByName"], landingpoint["name"].split(',')[0], landingpoint_instance)
    if landingpoint["name"].split(',')[0] == "Siyazan":
        print("#####")

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


#utility functions
def formatLength(length):
    """
    format the csv length
    """
    if length == "n.a.":
        return 0

    length = length.split(" ")
    return float(length[0].replace(",", ""))


# graph creation functions
def __addNode(catalog, landingpoint_id):
    """
    Add a node to the graph
    """
    if not gr.containsVertex(catalog["Graph"], landingpoint_id):
        gr.insertVertex(catalog["Graph"], landingpoint_id)


def __addEdge(catalog, origin, destination, length):
    """
    Ad an edge between two nodes
    """

    edge_check = gr.getEdge(catalog["Graph"], origin, destination)

    if edge_check is None:
        gr.addEdge(catalog["Graph"], origin, destination, length)