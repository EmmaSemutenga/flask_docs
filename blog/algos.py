factors = []
for n,m in zip(range(2,60), range(2,96)):
    if 60%n == 0 and 96%n == 0:
        factors.append(n)

print(max(factors)) 