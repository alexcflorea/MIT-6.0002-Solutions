###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Alex Florea
# Collaborators: None
# Time: 4:00

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================


# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    dataFile = open(filename, 'r')
    cows = {}
    for line in dataFile:
        line = line.rstrip().split(',')
        cows[line[0]] = int(line[1])
    dataFile.close()
    
    return cows


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    trips, trip, totalWeight = [], [], 0
    cowsCopy = dict(sorted(cows.items(), key=lambda weight: weight[1], reverse = True))

    while cowsCopy:
        for cow in cowsCopy:
            if (totalWeight + cowsCopy[cow]) <= limit:
                totalWeight += cowsCopy[cow]
                trip.append(cow)
                
        [cowsCopy.pop(cow) for cow in trip]            
        totalWeight = 0
        trips.append(trip)
        trip = []
        
    return trips


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cowsCopy = cows.copy()
    partitionList = []
    
    #Creates a partition (not necessarily in shortest length order)
    for partition in get_partitions(cowsCopy.keys()): 
        #Bool to ensure all elements in partition are under weight limit
        underWeightLimit = True
        
        #Picks out one trip of cows from partition
        for cowList in partition:
            totalWeight = 0
            
            #Looks at each cow on the trip and adds to list
            for cow in cowList:
                totalWeight += cowsCopy[cow]
                
                #If total weight is ever too high breaks out 
                #of the loop and sets check to False
                if totalWeight > limit:
                    underWeightLimit = False
                    break
            
        if underWeightLimit:
            partitionList.append(partition)
    
    
    partitionList = sorted(partitionList, key = lambda x: len(x))
    return partitionList[0]
            
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    
    FILE_NAME = 'ps1_cow_data.txt'
    cows = load_cows(FILE_NAME)
    
    start = time.time()
    greedy = greedy_cow_transport(cows)
    end = time.time()
    print('Greedy Algorithm determined', len(greedy), 'trips in', end-start, 'seconds\n')
    
    start = time.time()
    brute = brute_force_cow_transport(cows)
    end = time.time()
    print('Brute Force Algorithm determined', len(brute), 'trips in', end-start, 'seconds\n')

if __name__ == '__main__':
    compare_cow_transport_algorithms()