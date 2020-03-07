# dipendenze: pandas, xlrd

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# File excel con le distanze e i punti vendita
def read_excel(filename, mapIndex, truck_capacity):
    pv = pd.read_excel(filename, sheet_name='DomandaGiorno18')
    distWare = pd.read_excel(filename, sheet_name='DistanzaBase')
    baseCarico = pd.read_excel(filename, sheet_name='BaseCarico')
    distMatrix = pd.read_excel(filename, sheet_name='MatriceDistanze')
    domandaGiorno = pd.read_excel(filename, sheet_name='DomandaGiorno18')
    
    # Definizione della quantità di pv
    nb_customers = len(pv["CodicePV"])

    customers = pv["CodicePV"].tolist()

    # Creazione della distance_warehouses
    distance_warehouses = distWare["Distanza"].tolist()

    # # Truck capacity
    # truck_capacity = 39
    
    # Demands
    demands = []
    demandsTemp = domandaGiorno["Qta"].tolist()
    pvDD = domandaGiorno["CodicePV"].tolist()
    k = 0
    for n in range(0,len(customers)):
        if(pvDD[k] == customers[n]):
            demands.append(demandsTemp[k])
            k += 1
        else:
            demands.append(0)

    # Distance_matrix
    pv1 = distMatrix["pv1"].tolist()
    pv2 = distMatrix["pv2"].tolist()
    distances_pv = distMatrix["Distanza"].tolist()
    distance_matrix = []
    temp = []

    # Trovo tutti gli indici dei pv1 della domanda giornaliera dentro la Matrice delle distanze
    index_pvDD = []
    for pVendita in pvDD:
        indices = [i for i, x in enumerate(pv1) if x == pVendita]
        index_pvDD.append(indices)
        indices = []


    # Calcolo matrice distanze dei pv giornalieri lista di liste
    for j in range(0, len(index_pvDD)):
        for h, v1 in enumerate(pvDD):
            for o, v2 in enumerate(pvDD):
                for x, idx in enumerate(index_pvDD[j]):
                    if(v1 == pv1[idx] and v2 == pv2[idx]):
                        temp.append(distances_pv[idx])
                    elif(v1 == v2):
                        temp.append(0)
        distance_matrix.append(temp)
        temp = []

    # Elimino zeri e doppioni mantenendo l'ordine
    for j,dist in enumerate(distance_matrix):
        distance_matrix[j] = list(dict.fromkeys(dist))
    
    # for k,l in enumerate(distance_matrix):
    #     print (len(distance_matrix[k]))

    customers.insert(0,"434")

    for n, c in enumerate(customers):
        mapIndex[str(n + 1)] = str(c)

    return (nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, mapIndex)
            


# read_excel("distanze.xls")
