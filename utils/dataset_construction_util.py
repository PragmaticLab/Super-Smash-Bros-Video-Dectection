import logging
import os 
import random


def get_files_from_dir(mydir):
	return os.listdir(mydir) 

def generate_basic_image_dataset(posDir, negDir):
	positiveDirs = getFilesFromDir(posDir)
	negativeDirs = getFilesFromDir(negDir)
	negativeDirs = random.sample(negativeDirs, len(positiveDirs))


