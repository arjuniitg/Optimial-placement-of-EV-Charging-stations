import numpy as np
import matplotlib.pyplot as plt
from ypstruct import structure
import ga
import oct

dmd = oct.dmd
dist_bw_pts = oct.dist_bw_pts


#cost fun
# def obj_fun(arr):
#     res = 0
#     for ele in arr:
#         for i in range(1,25):
#             res += dmd[i] * min(  dist_bw_pts(ele[1],i) + ele[3]   ,   dist_bw_pts(ele[2],i) + ele[4]  )
#     return res

def obj_fun(arr):
    res = 0
    for i in range(1,25):
        dst_nrst_cs = 99999999999999
        for ele in arr:
            dst_nrst_cs = min( dist_bw_pts(ele[1],i) + ele[3]   ,   dist_bw_pts(ele[2],i) + ele[4] , dst_nrst_cs)
        res += dmd[i] * dst_nrst_cs
    return res



#problem definition
problem = structure()
problem.costfunc = obj_fun
problem.nvar = 2                #inputs the number of new charging stations taken as decision variable      # Decision Variable
problem.nold = 4


#GA Parameters
params = structure()
params.maxit = 100         #max no of iterations to perform
params.npop = 10        #inital population size
params.pc = 1           #proportion of children to main population     pc = 1 means #of children = #of other members in total population
params.mu = 0.30         #on an average, to change one gene out of 4 we should keep mu near to 25%. Although its randomized at mutation fun end so can be 0 or may be all 4!
#Run GA
out = ga.run(problem, params)
# finalgraph = oct.citigraph
# for ele in out.bestsol['position']:
#     finalgraph[ele[0]] = {ele[1]: ele[3], ele[2]: ele[4]}
#     finalgraph[ele[1]][ele[0]] = ele[3]
#     finalgraph[ele[2]][ele[0]] = ele[4]
# for ele in out.bestsol['position']:
#     del finalgraph[ele[1]][ele[2]]
#     del finalgraph[ele[2]][ele[1]]

print(0)
#Results

# printing network graph
# from pyvis.network import Network
# import networkx as nx
# net = nx.cycle_graph(10)
# #add nodes
# for ele in finalgraph:
#     if isinstance(ele,int):
#         net.add_node(ele,shape='circle',size=10)
#     else:
#         net.add_node(ele,shape='box',size=15,)
# for ele in finalgraph:
#     for edge in finalgraph[ele]:
#         net.add_edge(ele,edge,weight=finalgraph[ele][edge])
# nt = Network('800px','1200px')
# nt.from_nx(net)
# nt.toggle_physics(True)
# nt.show('nx.html')


# plt.plot(out.bestcost)
plt.semilogy(out.bestcost)
plt.xlim(0, params.maxit)
plt.xlabel('Iterations')
plt.ylabel('Best Cost')
plt.title('EV Iterations using GA')
plt.grid(True)
plt.show()