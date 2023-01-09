
def targetCorrect(target):
    """Takes a target number in standard format and converts it to match the wiring of each room"""

    # Rerouting algorithm
    if(target >= 16):
        # Room 3 and 4 Correction
        return (target // 8)*8 + 7 - (target % 8)

    if(target >= 8 and target % 8 != 0):
        # Room 2 correction
        return target + 8 - 2*(target % 8)

    return target

for target in range(16, 24):
    print(target) 
    print(targetCorrect(target))
    print(" ")