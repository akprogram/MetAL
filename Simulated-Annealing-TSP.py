#  به نام خدا
# Akbar Ghaedi: @1403-09-03..@1403-09-09.v2.1
# SA: Simulated Annealing Homework: TSP Problem
# prof: Dr. Salimifard
# TA: Mr. Tangsir Asl
# Metahuristic and AI
# pgu.ac.ir
# ciiorg.pgu.ac.ir

'''
sample solution:
    --------------
    SHOW_HELP = False
    Alphabetic_Phenotype = True

    Cities Distance:
    [[ 0  2  9 10  7]
    [ 2  0  6  4  3]
    [ 9  6  0  8  5]
    [10  4  8  0  6]
    [ 7  3  5  6  0]]
    Cities Count: 5

    Simulated Annealing Parameters:
      Max_Iteration = 5
      Init_Temperature = 250


    ------- Final Result -------
    Max_Iteration = 5
    first iteration of Find Best Solution = 0
    best Fitness = 26
    best Solution = [[ D B A E C ]]
'''
import math
import random
import numpy as np

SHOW_HELP = True        # show some comments to report program working
# SHOW_HELP = False

# TSP:
#   Phenotype:
#     Cities: A, B, C, D, E, F
#     Cities Distance:
#       As 2D Matrix:

citiesDistance = np.mat([[ 0,  2,  9, 10,  7],
                         [ 2,  0,  6,  4,  3],
                         [ 9,  6,  0,  8,  5],
                         [10,  4,  8,  0,  6],
                         [ 7,  3,  5,  6,  0]])

# Genotype:
#   We can use Alphabetic or numeric characters, so
#   List of chain/string of cities: [ - - - - - ]
#     example [ A B C D E ] or [ 0 1 2 3 4 ]

Alphabetic_Phenotype = True       # show cities as Alphabelt Characters. example: A B C...
# Alphabetic_Phenotype = False    # show cities as numeric Characters. example: 0 1 2...

# Simulated Annealing Parameters:
Init_Temperature = 250
Max_iteration = 5

def SimulatedAnnealing():   # The main function to run Simulated Annealing algorithm

  help(f"----- initialization -----")
  curSolution = CreateInitializationSolution()      # creation of the first route randomly at initial
  help(f"curSolution = {gpm(curSolution)}\n")
  bestSolution = curSolution                        # seting the first solution(Route) as a best solution at initial
  bestFitness = CalculateRouteLength(curSolution)   # seting the first solution fitness(Route Length) as a best fitness at initial

  tFindBestSolution = 0
  t = 0   # loop iteration

  # loop to find best solution
  help(f"----- loop to find best solution -----\n")
  while(t < Max_iteration):
    t += 1
    help(f"----- iteration: {t} -----")

    newSolution = CreateNeighbor(curSolution)     # get nearest neighbor
    help(f"newSolution: {gpm(newSolution)}")

    newFitness, curFitness = CalculateRouteLength(newSolution, "new Fitness"), CalculateRouteLength(curSolution, "curSolution")   # calculation of fitness of current & new solutions
    help(f"newFitness = {newFitness}")

    dE = newFitness - curFitness    # default: Minimization problem
    help(f"dE = {dE}")
    if dE <= 0:                     # << Intensification >> mechanism: Accepting the solution that improves fitness
      curSolution = newSolution
      if newFitness < bestFitness:  # default: Minimization problem
        bestSolution = newSolution  # keep the best solution
        bestFitness = newFitness    # keep fitness of best solution as betFitness
        tFindBestSolution = t       # the iteration that was found the best solution
        help(f"best: solution = {gpm(bestSolution)}\tfitness = {bestFitness}\tFindBestSolution: {tFindBestSolution}" )
    else:
      T = GetTemperature(t)     # Get the Temperature: Temperature is a criterion to create the probability of Bad solution Acceptation
      help(f"Temprature = {T}")
      if random.random() < math.exp(-dE / T):     # << Diversification >> mechanism: Accepting some bad solution randomly
        curSolution = newSolution
        help(f"Accept bad solution: {gpm(curSolution)}")
    help()
  return bestSolution, bestFitness, t, tFindBestSolution

def GetTemperature(t):    # Generate temperature value based on iteration
  if t < 3:
    return Init_Temperature
  return Init_Temperature / math.log2(t)    # logarithmic timeing

def CreateNeighbor(solution):
  neighbor = solution[:]    # copy solution as neighbor to change 2 member location at next lines: SAWP mechanism
  i, j = random.sample(range(len(solution)), 2)     # generate/select 2 random numbers from 0 to len(solution)-1 (example: 0..4) to exchange members
  neighbor[i], neighbor[j] = neighbor[j], neighbor[i]   # Swap mechanism to change 2 members of solution
  return neighbor

def CreateInitializationSolution():
  # creation of first route(solution) randomly
  route = [i for i in range(len(citiesDistance))]   # creation of route as 0..n, n = cities count. example route = [ 0 1 2 3 4 ]
  random.shuffle(route)    # shuffle list order: to create random solution(route) at first time
  return route

def CalculateRouteLength(route, name="route"):
  cirRoute = route + [route[0]]    # insert first city to end of route to simulate path circulation
  routeCitiesDistance = citiesDistance[cirRoute[:-1], cirRoute[1:]]   # selection of route distance vector by numpy advanced indexing
  routeLength = np.sum(routeCitiesDistance)   # route length calculation
  help(f"{name}: {gpm(route)}\t routeLength: {routeLength} = {' + '.join(str(dis) for dis in routeCitiesDistance.flat)}")
  return routeLength

def gpm(routes):    # Genotype-to-Phenotype Mapping
  if not Alphabetic_Phenotype:      # show cities as chain numbers: [ 0 1 2 3 4 ]
    return routes
  if (len(routes) > 0) and isinstance(routes[0], int):    # Changes [ 0 1 2 3 4 ] to [[ 0 1 2 3 4 ]] to be able to show a list of multiple paths
    routes = [routes]
  return str([ShowRouteAsAlphabet(route) for route in routes]).replace("'", "")

def ShowRouteAsAlphabet(route):   # show cities as the chain Alphabet characters: [ A B C D E ]
  return "[ " + " ".join(chr(ord("A") + cityId) for cityId in route) + " ]"

def help(*args, **kwargs):    # show comments if SHOW_HELP switch is True
  if SHOW_HELP:
      print(*args, **kwargs)

# ------------------
print(f"SHOW_HELP = {SHOW_HELP}")
print(f"Alphabetic_Phenotype = {Alphabetic_Phenotype}")
print()

print(f"Cities Distance: \n", citiesDistance)
print(f"Cities Count: {len(citiesDistance)}")
print()

print(f"Simulated Annealing Parameters:")
print(f"\tMax_Iteration = {Max_iteration}")
print(f"\tInit_Temperature = {Init_Temperature}")
print()

#------------ Run Program: Run SimulatedAnnealing() function to search Best Solution ------------
bestSolution, bestFitness, iteration, tFindBestSolution = SimulatedAnnealing()
print()

print("------- Final Result -------")
print(f"Max_Iteration = {Max_iteration}")
print(f"first iteration of Find Best Solution = {tFindBestSolution}")
print(f"best Fitness = {bestFitness}")
print(f"best Solution = {gpm(bestSolution)}")

#----- End of program -----
