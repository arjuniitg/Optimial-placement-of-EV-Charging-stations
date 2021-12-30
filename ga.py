from ypstruct import structure
import numpy as np
import random
import oct
def run(problem, params):
    global citigraph
    citigraph = oct.citigraph
    global dist_bw_pts
    dist_bw_pts = oct.dist_bw_pts
    #problem info
    costfunc = problem.costfunc
    global nvar
    nvar = problem.nvar
    global nold
    nold = problem.nold
    # varmin = problem.varmin
    # varmax = problem.varmax

    #parameters
    maxit = params.maxit
    npop = params.npop
    pc = params.pc
    nc = int(np.round(pc*npop/2)*2)      #this is to make nc an even no. everytime
    mu = params.mu                  # mu is used to choose on what gene mutation should be done

    # empty indivisual template
    empty_indivisual = structure()      #creates a structure for the chromosome
    empty_indivisual.position = None
    empty_indivisual.cost = None

    #keeping track of best solution ever found
    bestsol = empty_indivisual.deepcopy()       #we did deepcopy() as we do not want changes in bestsol to reflect upon empty_indivisual
    bestsol.cost = float('inf')     #since this is a minimization problem hence we will give cost of best sol to be infinity and change over iterations


    #edits
    global temp_weight

    #initialize population
    pop = empty_indivisual.repeat(npop)     #repeats the structure of a chromosome 'npop' times to create population
    #now we need to randomly position each chromosome to a point in our search space
    global old_cs
    for i in range(npop):
        pop[i].position = []

        #edits
        pop[i].position.extend([['c1',8,6,0,3],['c2',12,3,0,6],['c3',16,8,0,8],['c4',23,14,0,6]])
        temp_weight = [1]*24
        
        old_cs = [8,12,16,23]
        for ele in old_cs:
            temp_weight[ele-1] = 0

        for j in range(nold+1,nold+nvar+1):
            [temp] = random.choices(population=[i for i in range(1,25)], weights=temp_weight, k=1)
            temp2 = random.choice(list(citigraph[temp].keys()))
            temp3 = random.randint(0,dist_bw_pts(temp,temp2)-1)
            temp4 = dist_bw_pts(temp,temp2) - temp3
            pop[i].position.append(['c{}'.format(j) ,temp, temp2, temp3,temp4])

        # for j in range(1,nvar+1):
        #     temp = random.randint(1,24)
        #     temp2 = random.choice(list(citigraph[temp].keys()))
        #     temp3 = random.randint(0,dist_bw_pts(temp,temp2))
        #     temp4 = dist_bw_pts(temp,temp2) - temp3
        #     pop[i].position.append(['c{}'.format(j) ,temp, temp2, temp3,temp4])

        pop[i].cost = costfunc(pop[i].position)
        if pop[i].cost < bestsol.cost:
            bestsol = pop[i].deepcopy()     #again deepcopy as we do no want bestsol to change again n again when pop[i] changes

    # lets keep track of best cost over each iterations using an array-   'bestcost'
    bestcost = np.empty(maxit)

    # Main Loop
    for it in range(maxit):

        popc = []   #stores the children obtained after crossover/mutation operations, whose no. is decided by param 'pc'
        for _ in range(nc//2):

            #select parents randomly
            q = np.random.permutation(npop) #creates array of random nos 0 to npop which occur only once
            p1 = pop[q[0]]      #parent 1
            p2 = pop[q[1]]      #parent 2

            # Crossover operation with output chilren c1,c2
            c1, c2 = crossover(p1,p2)

            # Mutation operation
            c1 = mutate(c1, mu)
            c2 = mutate(c2, mu)

            # Evaluate first offspring
            c1.cost = costfunc(c1.position)
            if c1.cost < bestsol.cost:
                bestsol = c1.deepcopy()

            # Evaluate second offspring
            c2.cost = costfunc(c2.position)
            if c2.cost < bestsol.cost:
                bestsol = c2.deepcopy()

            # Add offsprings to population
            popc.append(c1)
            popc.append(c2)

        # Merge, sort and Select
        pop += popc
        pop.sort(key= lambda x:x.cost)      #sorting to only keep the min values on the top
        pop = pop[0:npop]                   #as we will only keep 'npop' population at a time hence slice the top best ones

        # store best cost
        bestcost[it] = bestsol.cost

        #Show Iteration info
        print('Iteration:{} , Best results at {}'.format(it,bestcost[it]),end=' ')
        print('at CS loc:',bestsol)
    print('Last Iteration:{} , Best results at {}'.format(it,bestcost[it]),end=' ')
    print('at CS loc:',bestsol)



    #output -  this hold the results that are being generated
    out = structure()
    out.pop = pop
    out.bestsol = bestsol
    out.bestcost = bestcost
    return out

def crossover(p1,p2):
    c1 = p1.deepcopy()  #as we want the structure of children to be same as that of a parent
    c2 = p2.deepcopy()

    #edits- changed i here
    i = random.randint(nvar+1,nvar+nold-1)     #randomly takes a point to crossover   # we're basically grouping and trying different locations of CS here
    
    c1.position , c2.position = c1.position[:i]+c2.position[i:] , c2.position[:i]+c1.position[i:]
    return c1,c2

def mutate(x, mu):
    y = x.deepcopy()        #copying the structure of x to the result y

    flag = np.random.rand(len(x.position)) <= mu   # an array of boolean T/F flags where we need to perform mutation (True only if its less than mu)
    
    #edits      # prevent from making changes to old cs positions
    for i in range(len(old_cs)):
        flag[i] = False


    ind = np.argwhere(flag)                  #   store array of indexes where flag is True
    ind = [item for sublist in ind for item in sublist]

    #edits
    for idx in ind:
        [temp] = random.choices(population=[i for i in range(1,25)], weights=temp_weight, k=1)
        temp2 = random.choice(list(citigraph[temp].keys()))
        temp3 = random.randint(0, dist_bw_pts(temp, temp2))
        temp4 = dist_bw_pts(temp, temp2) - temp3
        y.position[idx][1],y.position[idx][2],y.position[idx][3],y.position[idx][4] = temp,temp2,temp3,temp4
    return y