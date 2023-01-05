
for target in range(8, 24):
    print(target) 
    
    if(target >= 8 and target % 8 != 0):
        target = target + 8 - 2*(target % 8)
    
    print(target)
    print(" ")

targets = [1, 2]

print(targets)