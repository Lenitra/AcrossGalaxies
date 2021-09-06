# cost = [10, 5, 5]
# cost = [4, 9, 7]
cost = [10, 8, 2]

lvl = 10

for _ in range(lvl-1):
        cost[0] += cost[0]/2
        cost[1] += cost[1]/2
        cost[2] += cost[2]/2
cost[0] = int(cost[0])
cost[1] = int(cost[1])
cost[2] = int(cost[2])
print(cost)