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
from DISClib.ADT import graph as gr
from DISClib.ADT import stack as st
from DISClib.ADT import minpq as pq


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
    print("2- Identificar los clústeres de comunicación")
    print("3- Identificar los puntos de conexión críticos de la red")
    print("4- Ruta de menor distancia entre dos paises")
    print("5- Identificar la Infraestructura Crítica de la Red")
    print("6- Impacto de fallo en landing point")
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
        catalog, first_landingpoint, last_country = controller.initialize()
        print("Numero de landing points:", mp.size(catalog["LandingPoints"]))
        print("Numero de conexiones entre landing points:", gr.numEdges(catalog["Graph"]))
        print("Numero de paises:", mp.size(catalog["Countries"]))
        print("Primer landing point:")
        print("\tId:", first_landingpoint["id"].strip())
        print("\tNombre:", first_landingpoint["name"].strip())
        print("\tLatitude:", first_landingpoint["latitude"].strip())
        print("\tLongitude:", first_landingpoint["longitude"].strip())
        print("Ultimo pais:")
        print("\tNombre:", last_country["CountryName"].strip())
        print("\tPoblacion:", last_country["Population"].strip())
        print("\tUsuarios de internet:", last_country["Internet users"].strip())

    elif int(inputs[0]) == 2:
        #Requerimiento1
        landingpoint1 = input("Landing point 1:\n").strip()
        landingpoint2 = input("Landing point 2:\n").strip()

        clusters, connected = controller.req1(catalog, landingpoint1, landingpoint2)


        print("\nNumero de clusters:", clusters)
        print("Mismo cluster:", ("si" if connected else "no"))


    elif int(inputs[0]) == 3:
        #Requerimiento2
        ans = controller.req2(catalog)

        print("Lista de Landing points que sirven como puntos de interconexión")
        for key in ans:
            print("Landing point:", ans[key][0])
            print("\tPais:", ans[key][1])
            print("\tId:", ans[key][2])
            print("\tCables connectados:", ans[key][3])


    elif int(inputs[0]) == 4:
        #Requerimiento3
        paisA = input("Pais A:\n").strip()
        paisB = input("Pais B:\n").strip()

        res = controller.req3(catalog, paisA, paisB)

        if res == -1:
            print("Informacion de pais no se pudo validar")
            continue
        if res == False:
            print("No hay conexion entre estos dos paises")
            continue

        dist, route = res

        while not st.isEmpty(route):
            val = st.pop(route)
            print("\nId1:", val["vertexA"], "Id2:", val["vertexB"], "Distancia:", val["weight"], "km")

        print("Distancia Total:", dist, "km")


    elif int(inputs[0]) == 5:
        #Requerimiento4
    
        print("Este requerimiento no se puede completar debido a que la implementacion de prim no es correcta.")


    elif int(inputs[0]) == 6:
        #Requerimiento5
        landingpoint = input("Landing point:\n").strip()

        ans = controller.req5(catalog, landingpoint)

        print("Paises afectados:", pq.size(ans))
        print("\nLista de paises afectados:")

        while not pq.isEmpty(ans):
            val = pq.delMin(ans)
            print("\tPais:", val[0], "- Distancia:", val[1])

    

    else:
        sys.exit(0)

sys.exit(0)