from collections import defaultdict


def get_bus_U(state):
	return sum([q_table[dest] * prob for dest, prob in bus_stops[state]])

def get_U(state, action):
        if action == 0:
                return rewards[state] + gamma * q_table[state]
        else:
                return rewards[state] + gamma * get_bus_U(state)

def get_arr(policy):
        print(len(policy))
        print(policy)
        arr = []
        dic = {v: {u: p for u,p in t} for v, t in bus_stops.items()}
        print(dic)
        for i, a in enumerate(policy):
                if a == 0:
                        arr.append([-1 if j == i + 1 else (1 if j == i else 0) for j in range(len(policy))])
                else:
                        arr.append([-gamma*dic[i][j] if i in bus_stops.keys() and j in dic[i] else (1 if j == i else 0) for j in range(len(policy))])
                arr[i].append(rewards_dict[i])                
        return arr

def GJ(arr):
        arr.sort(key=lambda x: x.index()
        print()
        for l in arr:
                print(l)

grid_size = 20

rewards_dict = defaultdict(lambda: -0.5)

fixed_rewards = {10: 3, 19: 10, 13: -3}

rewards_dict.update(fixed_rewards)

rewards = [rewards_dict[i] for i in range(grid_size)]

bus_stops = {3: [(5, 0.5), (2, 0.1), (7, 0.4)], 7: [(3, 1/3), (9, 2/3)], 11: [(14, 0.5), (12, 0.5)]}

q_table = [0 for i in range(grid_size)]

print(rewards)

gamma = 0.8
for _ in range(10000):
	for state in range(grid_size):
		if state == grid_size - 1:
			q_table[state] = rewards[state]
			continue

		future_utility = q_table[state+1]
		if state in bus_stops:
			future_utility = max(future_utility, sum([q_table[dest] * prob for dest, prob in bus_stops[state]]))
		q_table[state] = rewards[state] + gamma * future_utility

print(q_table)
for state in range(grid_size-1):
	if state not in bus_stops:
		print(state, "walk")
		continue
	bus_U = get_bus_U(state)
	if bus_U > q_table[state+1]:
		print(state, "bus")
	else:
		print(state, "walk")


q_table = [0 for i in range(grid_size)]


beta = 0.5

import random
for t in range(10000):
	alpha = 1/(t+1)

	for state in range(grid_size):
		action = 0
		if random.random() < beta and state in bus_stops:
			action = 1

		if state == grid_size - 1:
			future_U = 0
		else:
			future_U = get_bus_U(state) if action == 1 else q_table[state + 1]

		q_table[state] = alpha * q_table[state] + (1-alpha) * (rewards[state] + gamma * future_U)

print(q_table)

for state in range(grid_size-1):
	if state not in bus_stops:
		print(state, "walk")
		continue
	bus_U = sum([q_table[dest] * prob for dest, prob in bus_stops[state]])
	if bus_U > q_table[state+1]:
		print(state, "bus")
	else:
		print(state, "walk")


policy = [0 for i in range(grid_size)]


for _ in range(1):
        arr = get_arr(policy)
        GJ(arr)
        for l in arr:
                print(l)
##        new_U = [rewards[state] + gamma * q_table[state] if policy[state] == 0 or state not in bus_stops else rewards[state] + get_bus_U(state) for state in range(grid_size)]
##	q_table = new_U
##	for state in range(grid_size-1):
##		policy[state] = 1 if state in bus_stops and get_bus_U(state) > q_table[state+1] else 0
##print(q_table)
##print(get_bus_U(3))
##for i in range(grid_size):
##	print(i, policy[i])
