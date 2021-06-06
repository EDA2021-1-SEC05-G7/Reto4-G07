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
 """

import config as cf
import model
import csv
import os

from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim as pm
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.DataStructures import linkedlistiterator as lt_it
from DISClib.ADT import graph as gr
from DISClib.ADT import minpq as pq
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def initialize():
    """
    initialize and build the catalog with necessary data
    """
    catalog = model.newCatalog()
    __loadConnections(catalog)
    last_country = __loadCountries(catalog)
    first_landingpoint = __loadLandingPoints(catalog)

    return (catalog, first_landingpoint, last_country)

#Requerimiento1
def req1(catalog, landingpoint1, landingpoint2):
    landingpoint1 = mp.get(catalog["LandingPointsByName"], landingpoint1)["value"]["landing_point_id"]
    landingpoint2 = mp.get(catalog["LandingPointsByName"], landingpoint2)["value"]["landing_point_id"]

    cnt = 0
    checked = mp.newMap(numelements=14000, maptype='CHAINING')

    stupid = mp.keySet(catalog["LandingPoints"])["first"]
    while stupid:
        key = stupid["info"]
        stupid = stupid["next"]

        if mp.contains(checked, key):
            continue
        mp.put(checked, key, True)
        cnt += 1
        dfs_struct = dfs.DepthFirstSearch(catalog["Graph"], key)

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

    if mp.contains(catalog["LandingPointsByName"], comboA):
        dirA = mp.get(catalog["LandingPointsByName"], comboA)["value"]["landing_point_id"]

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

    #Este requerimiento no se puede completar debido a que la puta implementacion de prim esta mal y no sirve ninguna de las funciones


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

    stupid = mp.keySet(countries)["first"]
    min_pq = pq.newMinPQ(cmp_req5)
    while stupid:
        key = stupid["info"]
        stupid = stupid["next"]

        weight = mp.get(countries, key)["value"]

        pq.insert(min_pq, (key, weight))

    return min_pq

#Req5 cmp function
def cmp_req5(a, b):
    if a[1] > b[1]:
        return True
    return False

#Custom reverse function
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

#load the data from files
def __loadConnections(catalog):
    """
    Load the connections from the file
    """
    connections_file = os.path.join('Data','connections.csv')
    input_file = csv.DictReader(open(connections_file, encoding="utf-8"), delimiter=",")

    for connection in input_file:
        model.addConnection(catalog, connection)

def __loadCountries(catalog):
    """
    Load the country info from the file
    """
    countries_file = os.path.join('Data','countries.csv')
    input_file = csv.DictReader(open(countries_file, encoding="utf-8"), delimiter=",")
    last_country = None

    for country in input_file:
        last_country = country
        model.addCountry(catalog, country)

    return last_country

def __loadLandingPoints(catalog):
    """
    Load the landing poitns info from the fiel
    """
    landingpoints_file = os.path.join('Data','landing_points.csv')
    input_file = csv.DictReader(open(landingpoints_file, encoding="utf-8"), delimiter=",")
    first_landingpoint = None

    for landingpoint in input_file:
        if first_landingpoint is None:
            first_landingpoint = landingpoint
        model.addLandingPoint(catalog, landingpoint)

    return first_landingpoint

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo