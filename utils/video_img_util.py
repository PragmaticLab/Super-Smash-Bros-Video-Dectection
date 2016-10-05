import logging
import os 

from pytube import YouTube
import pylab
import numpy as np 
import matplotlib.pyplot as plt
import imageio
from PIL import Image

def download_video(vid_id, outputDir='/tmp'):
	if outputDir[-1] == '/':
		outputDir = outputDir[:-1] # removes / from dir
	outputLoc = outputDir + "/" + vid_id + ".mp4"
	if os.path.isfile(outputLoc):
		os.remove(outputLoc)
	url = "http://www.youtube.com/watch?v=%s" % (vid_id)
	# logging.debug(url)
	yt = YouTube(url)
	yt.set_filename(vid_id)
	video = yt.get('mp4', '360p')
	video.download(outputDir)
	logging.info("Loading video %s" % (vid_id))
	vid = imageio.get_reader(outputLoc, 'ffmpeg')
	return vid, outputLoc

def get_image_at_time(vid, time, time_unit="s", mult=29.97):
	# note, each second is 30 frame, +15 means +0.5s
	# print time, time * 30 + 15
	image = vid.get_data(int(time * mult) + 15) 
	return image 

def show_image(image):
	plt.imshow(image)
	plt.show()

def save_image(image, fileName='temp', outputDir='/tmp', removeIfExist=True):
	if outputDir[-1] == '/':
		outputDir = outputDir[:-1] # removes / from dir
	outputLoc = outputDir + "/" + fileName + ".png"
	if removeIfExist and os.path.isfile(outputLoc):
		os.remove(outputLoc)
	imageio.imwrite(outputLoc, image)

def read_image(imageDir, img_width=32, formatted=True):
	image = Image.open(imageDir)
	image = image.resize((img_width,img_width), Image.BILINEAR)
	image = np.array(image)
	if formatted:
		image = image.flatten()
		image = image.reshape((1,image.shape[0]))
	return image

def get_numpy_frames_for_video(vid_id, img_width=32):
	vid, outputLoc = download_video(vid_id)
	image_list = []
	for i in range(0, vid.get_length(), 10):
		image = vid.get_data(i)
		image = Image.fromarray(image)
		image = image.resize((img_width,img_width), Image.BILINEAR)
		image = np.array(image)
		image = image.flatten()
		image = image.reshape((1,image.shape[0]))
		image_list += [image]
	return np.concatenate(image_list)

def load_image_from_array(image_arr, img_width=32):
	image_arr = image_arr.reshape((img_width, img_width, 3))
	image = Image.fromarray(image_arr)
	return image

# vid, vid_loc = download_video("drBfsroVfeo")
# show_image(get_image_at_time(vid, 4))
# show_image(get_image_at_time(vid, 31))
# save_image(get_image_at_time(vid, 4))

# vid = get_numpy_frames_for_video("drBfsroVfeo")
