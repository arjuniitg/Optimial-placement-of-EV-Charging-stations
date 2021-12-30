citigraph = {
    1:{2:9,   3:6},
    2:{1:9,   6:8},
    3:{1:6,   4:6,  12:6},
    4:{3:6,   11:9, 5:3},
    5:{4:3,   9:8,  6:6},
    6:{2:8,   5:6,  8:3},
    7:{8:4,   18:3},
    8:{6:3,   9:16, 16:8,  7:4},
    9:{5:8,   8:4,  10:16},
    10:{9:4,  11:8, 15:9, 17:12,  16:6},
    11:{4:9,  12:9, 14:6,  10:8},
    12:{3:6,  11:9, 13:4},
    13:{12:4, 24:6},
    14:{11:6, 23:6, 15:8},
    15:{10:9, 14:8, 22:4, 19:4},
    16:{8:8,  10:6, 17:3, 18:4},
    17:{16:3, 10:12,19:3},
    18:{7:3,  16:4, 20:6},
    19:{17:3, 15:4,  20:6},
    20:{18:6, 19:6,  22:8, 21:9},
    21:{22:3, 24:4,  20:9},
    22:{15:4, 23:6,  21:3, 20:8},
    23:{14:6, 24:3,  22:6},
    24:{23:3, 13:6,  21:4},
}



import heapq


def dijkstra(graph, starting_vertex):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[starting_vertex] = 0
    pq = [(0, starting_vertex)]

    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            # Only consider this new path if it's better than any path we've
            # already found.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def dist_bw_pts(a,b):
    if b in list(citigraph[a].keys()):  #if there is a direct path bw a,b
        return citigraph[a][b]
    return dijkstra(citigraph,a)[b]
#to add - distance between two points(on edge or vertex)

#print(dijkstra(citigraph,10)[1])
# distance bw two vertices -->  dijkstra(citigraph,10)[1]

### adding location of charging stations
# CS = [('c1',9,8,6,10),('c2',12,11,6,3),('c3',10,15,4,5),('c4',22,20,2,6)]   #(ci,neighbour_node1,neighbour_node2,neighbour_node_dist1,neighbour_node_dist2)


# for ele in CS:
#     citigraph[ele[0]]= {ele[1]:ele[3],ele[2]:ele[4]}


### declaring top demand points
dmd = {1:0.44,2:0.28,3:0.10,4:0.12,5:0.46,6:0.52,7:0.31,8:0.16,9:0.50,10:0.43,11:0.57,12:0.49,13:0.25,14:0.80,15:0.41,16:0.54,17:0.60,18:0.69,19:0.20,20:0.29,21:0.41,22:0.58,23:0.65,24:0.24}




