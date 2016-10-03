import logging
import os 

from pytube import YouTube
import pylab
import matplotlib.pyplot as plt
import imageio

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

def get_image_at_time(vid, time, time_unit="s"):
	# note, each second is 30 frame, +15 means +0.5s
	# print time, time * 30 + 15
	image = vid.get_data(int(time * 29.97) + 15) 
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
	plt.imshow(image)
	plt.savefig(outputLoc)

# vid, vid_loc = download_video("imGtJeEG6cc")
# show_image(get_image_at_time(vid, 4))
# show_image(get_image_at_time(vid, 31))
# save_image(get_image_at_time(vid, 4))
