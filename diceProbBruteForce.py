import random

# Goal:
# Determine the probability of a set of outcomes based on virtual dice rolls,
# specifically to test different probabilities of multiple dice rolls and their averaged effect on the equation.

# The initial output should merely test a consistent random roll; such as verifying that rolling 1d20 should have a 5% chance on each number.
# Output should show how many rolls were made, and the percentage outcome for each number in the set.

def roll(min = 1, max = 20, n = 1): # Accepts the minimum / maximum number of the dice being rolled, and the number of rolls (n)
    out = [0] * max
    for i in range(n):
        out[random.randint(min, max)-1] += 1
    return out

def printOutput(dataSet = [0]): # Simply formats the rolls for better readability.
    for i in range(len(dataSet)):
        print(f"{i+1}: {dataSet[i]}")
    return

print("")
printOutput(roll(n = 100000))
#input("Press Enter to End...")