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
import datetime as dt
import tracemalloc
import time

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

def req1(catalog, landingpoint1, landingpoint2):
    
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    #req
    req = model.req1(catalog, landingpoint1, landingpoint2)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print("time",delta_time,"memory",delta_memory)
    return req

    

def req2(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    #req
    req = model.req2(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print("time",delta_time,"memory",delta_memory)
    return req

def req3(catalog, paisA, paisB):
    def req2(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    #req
    req = model.req3(catalog, paisA, paisB)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print("time",delta_time,"memory",delta_memory)
    return req

def req4(catalog):
    def req2(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    #req
    req = model.req4(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print("time",delta_time,"memory",delta_memory)
    return req

def req5(catalog, landingpoint):
    def req2(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    #req
    req = model.req5(catalog, landingpoint)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print("time",delta_time,"memory",delta_memory)
    return req


# funciones para pruebas de rendimiento

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory