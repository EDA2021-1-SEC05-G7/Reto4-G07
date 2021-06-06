"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def printMenu():
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- ")
    print("3- ")
    print("4- ")
    print("5- ")
    print("6- ")
    print("7- ")
    print("0- Salir")
    print("*******************************************")

catalog = None

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.ini()
        info = controller.loadData(catalog)
        numvertex = controller.totalVertex(catalog)
        numedges = controller.totalEdges(catalog)
        countries = mp.size(catalog["Countries"])
        print('Numero de Landing Pointa: ' + str(numvertex))
        print('Numero de conexiones entre Landing points: ' + str(numedges))
        print("Total de paises:", countries)
        print(info)


    
    elif int(inputs[0]) == 2:
        #Requerimiento1
        pass

    
    elif int(inputs[0]) == 3:
        #Requerimiento2
        pass
    
    
    elif int(inputs[0]) == 4:
        #Requerimiento3
        pass


    elif int(inputs[0]) == 5:
        #Requerimiento4
        pass

    
    elif int(inputs[0]) == 6:
        #Requerimiento5
        pass

    elif int(inputs[0]) == 7:
        #Requerimiento6Bono
        pass


    elif int(inputs[0]) == 8:
        #Requerimiento7Bono
        pass

    elif int(inputs[0]) == 9:
        #Requerimiento8Bono
        pass

    else:
        sys.exit(0)
sys.exit(0)
