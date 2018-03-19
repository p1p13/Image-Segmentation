class Node:
	def __init__(self, parent, rank = 0, size = 1):
		self.parent = 	parent
		self.rank = rank
		self.size = size

class Graph:
	def __init__(self, num):
		self.nodes = [Node(i) for i in range(num)]

	def size(self, index):
		return self.nodes[index].size

	def parent(self, index):
		cache_index = index
		while index != self.nodes[index].parent:
			index = self.nodes[index].parent
		#Path Compression
		self.nodes[cache_index].parent = index
		return index

	def merge(self, index1, index2):
		#union by rank
		if self.nodes[index1].rank > self.nodes[index2].rank:
			self.nodes[index2].parent = index1
			self.nodes[index1].size = self.nodes[index1].size + self.nodes[index2].size
		else:
			self.nodes[index1].parent = index2
			self.nodes[index2].size = self.nodes[index1].size + self.nodes[index2].size

			if self.nodes[index1].rank == self.nodes[index2].rank:
				self.nodes[index2].rank = self.nodes[index2].rank + 1



def create_edge(image, width, x1, y1, x2, y2, calculate_weight):
	id1 = y1 * width + x1
	id2 = y2 * width + x2
	weight = calculate_weight(image, id1, id2)
	return (id1, id2, weight)

def edges(image, width, height, calculate_weight):
	edges = []
	for x in range(width):
		for y in range(height):
			if x > 0:
				edges.append(create_edge(image, x, y, x-1, y, calculate_weight))

			if y > 0:
				edges.append(create_edge(image, x, y, x, y-1, calculate_weight))

	return edges	

def segment_graph(edges, num, c):
	graph = Graph(num)
	edges = sorted(edges, key = lambda edge : edge[2])
	threshold = [c] * num
	for edge in edges:
		parent1 = graph.find(edge[0])
		parent2 = graph.find(edge[1])
		if parent2 != parent1:
			if edge[2] <= min(threshold[parent1], threshold[parent2]):
				graph.merge(parent1, parent2)
				node = graph.find(parent1)
				threshold[node] = edge[2] + c / graph.nodes[node].size

	return graph
