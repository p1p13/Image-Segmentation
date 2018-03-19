from PIL import Image
from graph import edges, segment_graph
from smoothen import smoothen_image
from random import random
import numpy as np
import sys

def diff_rgb(img, x1, y1, x2, y2):
    r = (img[0][x1, y1] - img[0][x2, y2]) ** 2
    g = (img[1][x1, y1] - img[1][x2, y2]) ** 2
    b = (img[2][x1, y1] - img[2][x2, y2]) ** 2
    return np.sqrt(r + g + b)

def diff_grey(img, x1, y1, x2, y2):
    v = (img[x1, y1] - img[x2, y2]) ** 2
    return np.sqrt(v)

def generate_image(graph, width, height):
	random_color = lambda: (int(random()*255), int(random()*255), int(random()*255))
	colors = [random_color() for i in range(width*height)]

	img = Image.new('RGB', (width, height))
	image = img.load()
	for y in range(height):
	    for x in range(width):
	        comp = graph.parent(y * width + x)
	        image[x, y] = colors[comp]

	return img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)

if __name__ == '__main__':
	image = Image.open(sys.argv[3])
	sigma = float(sys.argv[1])
	k = float(sys.argv[2])
	size = image.size

	if image.mode == 'RGB':
		r, g, b = image.split()
		r = smoothen_image(r, sigma)
		g = smoothen_image(g, sigma)
		b = smoothen_image(b, sigma)
		new_image = (r, g, b)
		calculate_weight = diff_rgb
	else:
		new_image = smoothen_image(image, sigma)
		calculate_weight = diff_grey

	edges = edges(new_image, size[1], size[0], calculate_weight)
	graph = segment_graph(edges, size[0]*size[1], k)

	output_image = generate_image(graph, size[1], size[0])
	output_image.save(sys.argv[4])