###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Alex Florea
# Collaborators: None
# Time: 1:00
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #First Method does not use DP
    # result = 0
    # currentWeight = 0
    # for weight in egg_weights[::-1]:
    #     while (currentWeight + weight) <= target_weight:
    #         result+=1
    #         currentWeight += weight
    # return result

    
    #Second Method Using DP (the memo is irrelevant in this implementation
    #since egg_weights is sorted)
    if (egg_weights, target_weight) in memo:
        result = memo[(egg_weights, target_weight)]
        
    elif len(egg_weights) == 1:
        result = target_weight
    
    elif target_weight // egg_weights[-1] == 0:
        result = dp_make_weight(egg_weights[:-1], target_weight)
    
    elif egg_weights[-1] <= target_weight:
        toTake = target_weight // egg_weights[-1]
        result = toTake + dp_make_weight(egg_weights[:-1], target_weight%egg_weights[-1], memo)
         
    memo[(egg_weights, target_weight)] = result
    return result
        

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    
    
    egg_weights = (1, 4, 6, 10, 25)
    n = 99
    print("Egg weights = (1, 4, 6, 10, 25)")
    print("n = 99")
    print("Expected ouput: 6 (3 * 25 + 2 * 10 + 1 * 4 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    
    
    egg_weights = (1, 2, 100, 523, 525)
    n = 524
    print("Egg weights = (1, 2, 100, 523, 525)")
    print("n = 524")
    print("Expected ouput: 2 (1 * 523 + 1 * 1)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    
    egg_weights = (1, 2, 100, 521, 525)
    n = 524
    print("Egg weights = (1, 2, 100, 521, 525)")
    print("n = 524")
    print("Expected ouput: 3 (1 * 521 + 1 * 2 + 1 * 1)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()