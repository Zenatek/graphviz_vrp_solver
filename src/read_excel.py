# dipendenze: pandas, xlrd

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# File excel con le distanze e i punti vendita
def read_excel(filename, mapIndex, truck_capacity, demands_for_day):
    pv = pd.read_excel(filename, sheet_name=demands_for_day)
    distWare = pd.read_excel(filename, sheet_name='DistanzaBase')
    baseCarico = pd.read_excel(filename, sheet_name='BaseCarico')
    distMatrix = pd.read_excel(filename, sheet_name='MatriceDistanze')
    domandaGiorno = pd.read_excel(filename, sheet_name=demands_for_day)

    # Tempo da WH a PV
    time_wh_to_pv = distWare["Tempo"].tolist()
    pv_for_time = distWare["pv2"].tolist()
    
    # Definizione della quantità di pv
    nb_customers = len(pv["CodicePV"])
    customers = pv["CodicePV"].tolist()

    # Creazione della distance_warehouses
    dist_warehouses = distWare["Distanza"].tolist()
    
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
    # Time_matrix
    time_pv = distMatrix["Tempo"].tolist()
    timePV = []
    time = []

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
                    if(v1 == pv1[idx] and v2 == pv2[idx] and v1 != v2):
                        temp.append(distances_pv[idx])
                        time.append(time_pv[idx])

        distance_matrix.append(temp)
        timePV.append(time)
        temp = []
        time = []
    
    for n, el in enumerate(timePV):
        timePV[n].insert(n,"0")

    # Elimino zeri e doppioni mantenendo l'ordine
    for j,dist in enumerate(distance_matrix):
        distance_matrix[j].insert(j,0)
    
    # for k,l in enumerate(distance_matrix):
    #     print (len(distance_matrix[k]))
    # print("Lunghezza distance_matrix: " + str(len(distance_matrix)))
    #print("Lunghezza dist: " + str(distance_matrix[-11]))

    # Creazione della distance_warehouses
    distance_warehouses = []
    for p in pvDD:
        distance_warehouses.append(dist_warehouses[pv_for_time.index(p)])

    customers.insert(0,"434")

    for n, c in enumerate(customers):
        mapIndex[str(n + 1)] = str(c)

    return (nb_customers, truck_capacity, distance_matrix, distance_warehouses, dist_warehouses, demands, mapIndex, timePV, time_wh_to_pv, pv_for_time)
            


# read_excel("distanze.xls")
