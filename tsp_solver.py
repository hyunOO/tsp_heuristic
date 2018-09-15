import sys
import numpy as np
import random

# x is a list which contains the values of x coordinates
x = []
# y is a list which contains the values of y coordinates
y = []
# node is a total number of nodes
node = 0

filename = sys.argv[1]
file = open(filename, "r")

for i in range(6):
	file.readline()

while True:
	line = file.readline()
	if 'EOF' in line:
		break
	line_list = line.replace('\n', ' ').split(' ')
	count = 0
	for i in range(len(line_list)):
		elem = line_list[i]
		if elem != '':
			if count == 1:
				x.append(float(elem))
				node +=1
			elif count == 2:
				y.append(float(elem))
			else:
				pass
			count += 1

class Permutation:
	def __init__(self, permute, dist):
		self.permute = permute
		self.dist = dist

# random_permutation function returns a randomly generated permutation from 1 to integer value node
def random_permutation(node):
	x = [i for i in range(node)]
	random.shuffle(x)
	return x

# calcuate_distance function takes a role of fitness function
# However, I will use this function for comparing among individuals
def calculate_distance(node_list):
	dist = 0
	for i in range(len(node_list) - 1):
		dist += np.square(x[node_list[i + 1]] - x[node_list[i]]) + np.square(y[node_list[i + 1]] - y[node_list[i]])
	dist += np.square(x[node_list[len(node_list) - 1]] - x[node_list[0]]) + np.square(y[node_list[len(node_list) - 1]] - y[node_list[0]])
	return dist

# tournament_selection function proceeds tournament selection among 20 individuals
def tournament_selection():
	global node
	ran_individual = []
	for i in range(20):
		ran_individual.append(random_permutation(node))
	index = 0
	dist = calculate_distance(ran_individual[0])
	for i in range(19):
		new_dist = calculate_distance(ran_individual[i + 1])
		if new_dist < dist:
			dist = new_dist
			index = i + 1
	return Permutation(ran_individual[index], dist)

# longest_common function returns the longest common consecutive sequences between two lists
def longest_common(list1, list2):
	lcs = []
	index = 0
	for i in range(len(list1)):
		for j in range(len(list2)):
			if list1[i] == list2[j]:
				sub_lcs = []
				iteration_no = np.minimum(len(list1) - i, len(list2) - j)
				for k in range(iteration_no):
					if list1[i + k] == list2[j + k]:
						sub_lcs.append(list1[i + k])
					else:
						break
				if len(sub_lcs) > len(lcs):
					index = i
					lcs.clear()
					for elem in sub_lcs:
						lcs.append(elem)
	return (lcs, index)

def elitism(list1, list2):
	result = []
	for i in list1:
		result.append(i)
	for i in list2:
		result.append(i)
	result.sort(key = lambda x: x.dist)
	return result[20: ]

# diff function returns a list who is in list 1 but not in list2
def diff(list1, list2):
	set2 = set(list2)
	return [i for i in list1 if i not in list2]

# crossover function proceeds crossover between two individuals and returns a new child
def crossover(ind1, ind2):
	global node

	lcs, start_index = longest_common(ind1, ind2)
	end_index = start_index + len(lcs) - 1	

	rand1 = 0
	if start_index != 0:
		rand1 = random.randint(0, start_index)
	else:
		rand1 = random.randint(end_index + 1, len(ind1))
	rand2 = random.randint(np.maximum(rand1, end_index), len(ind1))

	answer = []
	for i in range(node):
		if start_index <= i and i <= end_index:
			answer.append(ind1[i])
		elif rand1 <= i and i <= rand2:
			answer.append(ind1[i])
		else:
			answer.append(ind2[i])
	return answer
	
population = []
child = []
for i in range(20):
	ts = tournament_selection()
	population.append(ts)
	print(ts.dist)
for k in range(200):
	print("hello")
	for i in range(19):
		child_permute = crossover(population[i].permute, population[i + 1].permute)
		child_ind = Permutation(child_permute, calculate_distance(child_permute))
		child.append(child_ind)
		print(child_ind.dist)
	child_permute = crossover(population[0].permute, population[19].permute)
	child_ind = Permutation(child_permute, calculate_distance(child_permute))
	child.append(child_ind)
	print(child_ind.dist)
	population = elitism(population, child)

