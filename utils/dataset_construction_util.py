import logging
import os 
import random
import numpy as np 
from video_img_util import read_image


def get_files_from_dir(mydir):
	return os.listdir(mydir) 

def generate_basic_image_dataset(posDir, negDir, sampleMultiplier=1):
	if posDir[-1] != '/':
		posDir += "/"
	if negDir[-1] != '/':
		negDir += "/"
	positiveDirs = get_files_from_dir(posDir)
	negativeDirs = get_files_from_dir(negDir)
	negativeDirs = random.sample(negativeDirs, int(len(positiveDirs) * sampleMultiplier))
	y_list = []
	x_list = []
	file_list = []
	img_width = 32
	# this prob should be refactored... but I am lazy atm
	for i in positiveDirs:
		imgDir = posDir + i
		img = read_image(imgDir, img_width)
		if img.shape[1] == 3 * img_width * img_width:
			y_list += [1]
			x_list += [img]
			file_list += [imgDir]
	for i in negativeDirs:
		imgDir = negDir + i
		img = read_image(imgDir, img_width)
		if img.shape[1] == 3 * img_width * img_width:
			y_list += [0]
			x_list += [img]
			file_list += [imgDir]
	X, y = np.concatenate(x_list), np.array(y_list)
	return X, y, file_list

