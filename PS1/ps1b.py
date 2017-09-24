###########################
# 6.0002 Problem Set 1b: Space Change
# Name: BOHDAN DRAHAN   
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
    # TODO: Your code here
    if weight_is_in_egg_weights(target_weight, egg_weights):
        return 1

    for  weight in range(1, target_weight +1):

        if weight_is_in_egg_weights(weight, egg_weights):
            memo[weight] = 1
            continue

        qty_eggs = weight
        for egg in egg_weights:
            if egg > weight:
                continue
            if memo[weight - egg] + 1 < qty_eggs:
                qty_eggs = memo[weight - egg] + 1
            memo[weight] = qty_eggs

    return memo[target_weight]

def weight_is_in_egg_weights(weight, egg_weights):
    if weight in egg_weights:
        return True
    else: return False


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print("\n")
    
    egg_weights = (1, 5, 10, 25)
    n = 25 
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 25")
    print("Expected ouput: 1")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print("\n")

    egg_weights = (1, 5, 10, 25)
    n = 4 
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 4")
    print("Expected ouput: 4")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print("\n")
