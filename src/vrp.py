########## cvrp.py ##########

import localsolver
import sys
import math

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

from read_excel import *
from results import *
from drawGraph import *


def read_elem(filename):
    with open(filename) as f:
        return [str(elem) for elem in f.read().split()]


def main(instance_file, str_time_limit, sol_file, str_nb_trucks, truck_capacity):
    nb_trucks = int(str_nb_trucks)
    mapIndex = {}
    #
    # Reads instance data
    #
    (nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, mapIndex) = read_excel(instance_file, mapIndex, int(truck_capacity))
    # The number of trucks is usually given in the name of the file
    # nb_trucks can also be given in command line

    if nb_trucks == 0:
        nb_trucks = get_nb_trucks(instance_file)

    with localsolver.LocalSolver() as ls:
        #
        # Declares the optimization model
        #
        model = ls.model

        # Sequence of customers visited by each truck.
        customers_sequences = [model.list(nb_customers) for k in range(nb_trucks)]

        # All customers must be visited by  the trucks
        model.constraint(model.partition(customers_sequences))
        
         # Create demands as an array to be able to access it with an "at" operator
        demands_array = model.array(demands)
        
         # Create distance as an array to be able to acces it with an "at" operator
        distance_array = model.array()

        for n in range(nb_customers):
            distance_array.add_operand(model.array(distance_matrix[n]))

        distance_warehouse_array = model.array(distance_warehouses)

        route_distances = [None for n in range(nb_trucks)]

        # A truck is used if it visits at least one customer
        trucks_used = [(model.count(customers_sequences[k]) > 0) for k in range(nb_trucks)]
        nb_trucks_used = model.sum(trucks_used)

        for k in range(nb_trucks):
            sequence = customers_sequences[k]
            c = model.count(sequence)
                        
            # Quantity in each truck
            demand_selector = model.function(lambda i: model.at(demands_array, sequence[i]))
            route_quantity = model.sum(model.range(0, c), demand_selector) 
            model.constraint(route_quantity <= truck_capacity)
            
            # Distance traveled by each truck
            dist_selector = model.function(lambda i: model.at(distance_array, sequence[i-1], sequence[i]))
            route_distances[k] = model.sum(model.range(1,c), dist_selector) + \
                 model.iif(c > 0, model.at(distance_warehouse_array, sequence[0]) + model.at(distance_warehouse_array, sequence[c-1]),0)                       
       
        # Total distance travelled
        total_distance = model.sum(route_distances)

        # Objective: minimize the number of trucks used, then minimize the distance travelled
        model.minimize(nb_trucks_used)
        model.minimize(total_distance)

        model.close()

        #
        # Parameterizes the solver
        #
        ls.param.time_limit = int(str_time_limit)

        ls.solve()

        #
        # Writes the solution in a file with the following format:
        #  - number of trucks used and total distance
        #  - for each truck the nodes visited (omitting the start/end at the depot)
        #
        if len(sys.argv) >= 3:
            with open("../results/" + sol_file, 'w') as f:
                f.write("%d %d\n" % (nb_trucks_used.value, total_distance.value))
                for k in range(nb_trucks):
                    if(trucks_used[k].value != 1): continue
                    # Values in sequence are in [0..nbCustomers-1]. +2 is to put it back in [2..nbCustomers+1]
                    # as in the data files (1 being the depot)
                    for customer in customers_sequences[k].value:
                        f.write("%d " % (customer + 2))
                    f.write("\n")

    # Write solution as pv id.
    write_results(mapIndex, "../results/" + sol_file)

    # Draw graph of track's route
    draw_graph("../results/" + sol_file, warehouse = "434")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Usage: python vrp.py input_file [output_file] [time_limit] [nb_trucks] [truck_capacity]")
        sys.exit(1)

    instance_file = sys.argv[1];
    sol_file =  sys.argv[2] if len(sys.argv) > 2 else None;
    str_time_limit = sys.argv[3] if len(sys.argv) > 3 else "20";
    str_nb_trucks = sys.argv[4] if len(sys.argv) > 4 else "0";
    truck_capacity = sys.argv[5] if len(sys.argv) > 5 else "39";
        
    main(instance_file, str_time_limit, sol_file, str_nb_trucks, truck_capacity)



