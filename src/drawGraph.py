from graphviz import Digraph
import random

def draw_graph(result_file, warehouse):
    route = []
    fileX = []
    nbTruck = ""
    total_distance = ""
    title = 'VRP solution'
    dot = Digraph(comment=title)
    dot.node(warehouse, warehouse)

    with open(result_file, "r") as fd:
        for line in fd:
            fileX.append(line.replace(" \n",""))
        fd.close()

    for n_pv, pv in enumerate(fileX):
        if(n_pv != 0):
            route = pv.split(" ")
            color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for node in route:
                dot.node(node,node, color=color)
            # draw fist edge. From warehouse to pv1
            dot.edge(warehouse, route[0],color=color)
            # draw all edge 
            for n,node in enumerate(route):
                if (n < len(route)-1):
                    dot.edge(route[n], route[n+1], color=color)
                else:
                    dot.edge(route[n], warehouse, color=color)
        else:
            route = pv.split(" ")
            route[1] = route[1].replace("\n","")
            nbTruck = str(route[0]) + "_"
            total_distance = str(route[1])
                


    dot.render("../results/" + title + "_" + nbTruck + total_distance + '.gv', view=True)  


#draw_graph("../result/", warehouse = "434")
