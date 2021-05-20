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


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def ini():

    return model.newCatalog()

# Funciones para la carga de datos

def loadData(catalog):
    loadConnections(catalog)
    loadCountries(catalog)
    loadLandingPoints(catalog)



def loadConnections(catalog):

    connectionsFile = os.path.join('Data','connections.csv')
    input_file = csv.DictReader(open(connectionsFile, encoding="utf-8"),
                                delimiter=",")

    for connection in input_file:
        model.addConnection(catalog, connection)



def loadCountries(catalog):

    countriesfile = os.path.join('Data','countries.csv')
    input_file = csv.DictReader(open(countriesfile, encoding="utf-8"),
                                delimiter=",")

    for country in input_file:
        model.addCountries(catalog, country)



def loadLandingPoints(catalog):

    landing_points_file = os.path.join('Data','landing_points.csv')
    input_file = csv.DictReader(open(landing_points_file, encoding="utf-8"),
                                delimiter=",")
    for landpoi in input_file:
        model.addLandingPoints(catalog, landpoi)
        


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def totalVertex(catalog):

    return model.totalVertex(catalog)



def totalEdges(catalog):

    return model.totalEdges(catalog)
