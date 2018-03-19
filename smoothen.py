import numpy as np
from scipy.signal import convolve2d

def gaussian_kernel(sigma, alpha):
	radius = int(n.ceil(sigma * alpha))
	x,y = np.mgrid[-radius : radius + 1, -radius : radius + 1]
	kernel = exp(-0.5 * (x ** 2 + y ** 2) / (sigma ** 2))
	return kernel / np.sum(kernel)

def smoothen_image(image, sigma, alpha = 4):
	kernel = gaussian_kernel(sigma, alpha)
	image =  asarray(image).astype('float')
	return convolve2d(image, kernel, mode = 'same')

