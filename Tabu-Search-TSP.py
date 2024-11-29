#  به نام خدا
# Akbar Ghaedi: @1403-09-03..@1403-09-09.v1.6
# TS: Tabu Search Homework: TSP Problem
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

    Tabu Search Parameters:
      Max_Iteration = 50
      tabuListSize = 3
      tabuList = deque([], maxlen=3)
    --------------
    ------- Final Result -------
    Best Route: [[ B A C E D ]]
    Best Route Length: 26
    The iteration of main TabuSearch Loop: 2
    The iteration that found Best Solution: 1
'''
import math
import random
import numpy as np
from collections import deque     # double-end queue: used for queue as auto FIFO queue management

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

# Tabu Search Parameters
Max_Iteration = 50
tabuListSize = 3
tabuList = deque(maxlen = tabuListSize)   # deque is a double-ended queue that remove the first member of the list if was full (FIFO mechanism), automatically in O(1) time complexity


def TabuSearch():
  # initialization
  currentRoute = CreateInitializationSolution()   # creation of initial route
  bestRoute = currentRoute      # set initial route as best solution
  bestRouteLength = CalculateRouteLength(bestRoute, "Initial Route")     # as a fitness function
  iBestSolution = 0   # number of last iteration that find best solution

  i = 0
  while(i < Max_Iteration):
    i += 1    # loop iteration counter
    help(f"\n----- iteration {i} -----")
    neighborList = GenerateNeighbors(currentRoute)    # creation of route neighbor list
    help(f"neighborList = {gpm(neighborList)}")

    # selection of the best solution from neighbor list: as local shortest route
    foundBestSolution = False     # To check that the best solution was found or break the main loop, if no better solution is found.
    for neighborRoute in neighborList:
      if neighborRoute not in tabuList:    # << Diversification >> mechanism: breaking the optimal local chain: avoiding of iterative solution
        neighborRouteLength = CalculateRouteLength(neighborRoute, "Current Route")    # fitness function
        if neighborRouteLength < bestRouteLength:    # << Intensification >> mechanism: selection of local best solution(shortest route)
          bestRoute = neighborRoute                  # assign this solution as a best route (solution)
          bestRouteLength = neighborRouteLength      # setting the best fitness
          currentRoute = bestRoute    # assign current route for next iteration neighbor creation
          iBestSolution = i           # keeping of counter where was found best solution
          foundBestSolution = True
          help(f"bestRoute: --> {gpm(bestRoute)}   bestRouteLength = {bestRouteLength}  <--")

    if foundBestSolution:
      AddMoveToTabuList(bestRoute)            # add this solution to tabulist, continuation of the << Diversification >> mechanism
    else:
      help(f"\nThe better neighbor was not found. So, break loop at {i} iterations.")
      break
  return bestRoute, bestRouteLength, iBestSolution, i

def AddMoveToTabuList(route):
  tabuList.append(route)  # deque remove first member of tabulist if tabulist is full (FIFO mechanism) automatically in O(1)
  # if len(tabuList) > tabuListSize:
  #   tabuList.pop(0)
  help(f"tabuList = {gpm(tabuList)}")

def CalculateRouteLength(route, name="route"):
  cirRoute = route + [route[0]]    # insert first city to end of route to simulate path circulation
  routeCitiesDistance = citiesDistance[cirRoute[:-1], cirRoute[1:]]   # selection of route distance vector by numpy advanced indexing
  routeLength = np.sum(routeCitiesDistance)   # route length calculation
  help(f"{name}: {gpm(route)}\t routeLength: {routeLength} = {' + '.join(str(dis) for dis in routeCitiesDistance.flat)}")
  return routeLength

def GenerateNeighbors(route):    # creation of route neighbor list
  '''
    creation of route neighbor list by 'SWAP' mechanism
    count of neighbors = C(n, 2)
    C(n, 2) = n(n-1)/2
    example: len(route) = 5
    C(5, 2) = 5(5 - 1)/2 = 5 * 4/2 = 10
  '''
  neighborList = []
  for i in range(len(route)):
    for j in range(i + 1, len(route)):
      neighbor = route[:]
      neighbor[i], neighbor[j] = neighbor[j], neighbor[i]     # swaping of tow neighbors to create nearest neighbor
      neighborList.append(neighbor)
  return neighborList

def CreateInitializationSolution():
  # creation of first route(solution) randomly
  route = [i for i in range(len(citiesDistance))]   # creation of route as 0..n, n = cities count. example for 5 cities, route = [ 0 1 2 3 4 ]
  random.shuffle(route)    # shuffle list order: to create random solution(route) at first time
  return route

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

print(f"Tabu Search Parameters:")
print(f"\tMax_Iteration = {Max_Iteration}")
print(f"\ttabuListSize = {tabuListSize}")
print(f"\ttabuList = {tabuList}")
print("--------------")
print()

# Run TabuSearch() function to search Best Solution
bestRoute, bestRouteLength, iBestSolution, iteration = TabuSearch()
print()
print("------- Final Result -------")
print(f"Best Route: {gpm(bestRoute)}")
print(f"Best Route Length: {bestRouteLength}")
print(f"The iteration of main TabuSearch Loop: {iteration}")
print(f"The iteration that found Best Solution: {iBestSolution}")

#----- End of program -----
