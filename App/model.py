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
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim as pm
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.DataStructures import linkedlistiterator as lt_it
from DISClib.ADT import graph as gr
from DISClib.ADT import minpq as pq
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos

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

# Funciones para agregar informacion al catalogo
 
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
    

# Funciones para creacion de datos

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


# Requerimientos

#Requerimiento1
def req1(catalog, landingpoint1, landingpoint2):

    #Se obtiene el Id de los dos landing points
    landingpoint1 = mp.get(catalog["LandingPointsByName"], landingpoint1)["value"]["landing_point_id"]
    landingpoint2 = mp.get(catalog["LandingPointsByName"], landingpoint2)["value"]["landing_point_id"]

    cnt = 0

    #Revisa si ya se pasa por un nodo
    checked = mp.newMap(numelements=14000, maptype='CHAINING')

    #Iterador manual
    stupid = mp.keySet(catalog["LandingPoints"])["first"]
    
    while stupid:
        key = stupid["info"]
        stupid = stupid["next"]

        #Revisa si la llave está en el map
        if mp.contains(checked, key):
            continue
        mp.put(checked, key, True)
        cnt += 1
        dfs_struct = dfs.DepthFirstSearch(catalog["Graph"], key)

        #segundo iterador manual

        stupid2 = mp.keySet(catalog["LandingPoints"])["first"]
        
        while stupid2:
            key2 = stupid2["info"]
            stupid2 = stupid2["next"]
            if mp.contains(checked, key2):
                continue

            if dfs.hasPathTo(dfs_struct, key2):
                mp.put(checked, key2, True)

    dfs_struct = dfs.DepthFirstSearch(catalog["Graph"], landingpoint1)

    return (cnt, dfs.hasPathTo(dfs_struct, landingpoint2))



#Requerimiento2
def req2(catalog):
    ans = {}

    #Iterador manual
    stupid = mp.keySet(catalog["LandingPoints"])["first"]

    while stupid:
        key = stupid["info"]
        stupid = stupid["next"]

        val = mp.get(catalog["LandingPoints"], key)["value"]
        name = val["name"].split(',')

        ans[key] = (
            name[0],
            "" if len(name) <= 1 else (name[1] if len(name) == 2 else name[1]+name[2]),
            val["id"],
            gr.indegree(catalog["Graph"], key) + gr.outdegree(catalog["Graph"], key)
        )

    return ans

#Requerimiento3
def req3(catalog, paisA, paisB):
    paisA = mp.get(catalog["Countries"], paisA)["value"]
    paisB = mp.get(catalog["Countries"], paisB)["value"]

    comboA = paisA["CapitalName"]+", " + paisA["CountryName"]
    comboB = paisB["CapitalName"]+", " + paisB["CountryName"]

    dirA = None
    dirB = None

    if mp.contains(catalog["LandingPointsByName"], comboA):
        dirA = mp.get(catalog["LandingPointsByName"], comboA)["value"]["landing_point_id"]

    if mp.contains(catalog["LandingPointsByName"], comboB):
        dirB = mp.get(catalog["LandingPointsByName"], comboB)["value"]["landing_point_id"]

    
    if dirA is None:
        stupid = mp.keySet(catalog["LandingPointsByName"])["first"]
        while stupid:
            key = stupid["info"]
            stupid = stupid["next"]

            name = mp.get(catalog["LandingPointsByName"], key)["value"]["name"]

            if paisA["CountryName"] in name:
                dirA = mp.get(catalog["LandingPointsByName"], key)["value"]["landing_point_id"]
                break

    if dirB is None:
        stupid = mp.keySet(catalog["LandingPointsByName"])["first"]
        while stupid:
            key = stupid["info"]
            stupid = stupid["next"]

            name = mp.get(catalog["LandingPointsByName"], key)["value"]["name"]

            if paisB["CountryName"] in name:
                dirB = mp.get(catalog["LandingPointsByName"], key)["value"]["landing_point_id"]
                break

    if dirA is None or dirB is None:
        return -1

    bf_struct = dj.Dijkstra(catalog["Graph"], dirA)

    if not dj.hasPathTo(bf_struct, dirB):
        return False

    dist = dj.distTo(bf_struct, dirB)
    route = dj.pathTo(bf_struct, dirB)

    return (dist, route)

#Requerimiento4
def req4(catalog):
    prim_struct = pm.PrimMST(catalog["Graph"])

    weight = pm.weightMST(prim_struct)

    return None

   

#Requerimiento5
def req5(catalog, landingpoint):
    landingpoint = mp.get(catalog["LandingPointsByName"], landingpoint)["value"]["landing_point_id"]

    graph = catalog["Graph"]
    rev_graph = __reverseGraph(graph)

    lst_adj = gr.adjacents(graph, landingpoint)
    lst_adj_rev = gr.adjacents(rev_graph, landingpoint)

    countries = mp.newMap(numelements=14000, maptype='CHAINING')

    for adj in lt.iterator(lst_adj):
        edge = gr.getEdge(graph, landingpoint, adj)['weight']
        country = mp.get(catalog["LandingPoints"], adj)["value"]["name"].split(",")[-1]
        if mp.contains(countries, country):
            if mp.get(countries, country)["value"] <= edge:
                continue
        mp.put(countries, country, edge)

    for adj_rev in lt.iterator(lst_adj_rev):
        edge = gr.getEdge(rev_graph, adj, landingpoint)['weight']
        country = mp.get(catalog["LandingPoints"], adj_rev)["value"]["name"].split(",")[-1]
        if mp.contains(countries, country):
            if mp.get(countries, country)["value"] <= edge:
                continue
        mp.put(countries, country, edge)

    #iterador manual
    stupid = mp.keySet(countries)["first"]
    min_pq = pq.newMinPQ(cmp_req5)
    while stupid:
        key = stupid["info"]
        stupid = stupid["next"]

        weight = mp.get(countries, key)["value"]

        pq.insert(min_pq, (key, weight))

    return min_pq



# Funciones utilizadas para comparar elementos dentro de una lista

def cmp_req5(a, b):
    if a[1] > b[1]:
        return True
    return False


# Funciones de ordenamiento



def formatLength(length):
    """
    format the csv length
    """
    if length == "n.a.":
        return 0

    length = length.split(" ")
    return float(length[0].replace(",", ""))


def __reverseGraph(graph):
    greverse = gr.newGraph(size=gr.numVertices(graph),
                          directed=True,
                          comparefunction=graph['comparefunction']
                          )

    lstvert = gr.vertices(graph)
    for vert in lt.iterator(lstvert):
        gr.insertVertex(greverse, vert)

    for vert in lt.iterator(lstvert):
        lstadj = gr.adjacents(graph, vert)
        for adj in lt.iterator(lstadj):
            weight = gr.getEdge(graph, vert, adj)["weight"]
            gr.addEdge(greverse, adj, vert, weight)
    return greverse


