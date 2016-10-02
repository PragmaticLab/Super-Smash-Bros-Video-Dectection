import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
sys.path.append("../utils/")
import os
import random
import math
import numpy as np 
import pandas as pd 

from video_img_util import download_video, get_image_at_time, save_image

inputCsv = sys.argv[1]
outputDir = sys.argv[2]


def get_negative_samples(curr_start_time, curr_end_time, curr_round_start, curr_round_end, n=5):
	seconds = range(curr_round_start, curr_round_end, 1)
	filtered_seconds = [s for s in seconds if math.fabs(s - curr_start_time) > 1 and math.fabs(s - curr_end_time) > 1]
	return random.sample(filtered_seconds, n)

def construct_image_dataset(vid, curr_vid_id, curr_start_time, curr_end_time, curr_round_start, curr_round_end):
	img_start = get_image_at_time(vid, curr_start_time)
	img_start_name = "1_%s_%s" % (curr_vid_id, curr_start_time)
	save_image(img_start, img_start_name, outputDir)

	img_end = get_image_at_time(vid, curr_end_time)
	img_end_name = "2_%s_%s" % (curr_vid_id, curr_end_time)
	save_image(img_end, img_end_name, outputDir)

	for neg_s in get_negative_samples(curr_start_time, curr_end_time, curr_round_start, curr_round_end):
		img_neg = get_image_at_time(vid, neg_s)
		img_neg_name = "0_%s_%s" % (curr_vid_id, neg_s)
		save_image(img_neg, img_neg_name, outputDir)

def generate_dataset(df):
	latest_vid_id = ""
	latest_vid, latest_vid_loc = None, None
	for index, row in df.iterrows():
		if index % 10 == 0: # simple logging 
			print "Generating %d / %d rounds of SMASH!" % (index, df.shape[0])

		curr_vid_id, curr_start_time, curr_end_time, curr_round_start, curr_round_end = row['vidid'], row['start_time'], row['end_time'], row['round_start'], row['round_end']
		if curr_vid_id != latest_vid_id: # need to reload the new video
			if latest_vid_loc:
				logging.info("Deleting old vid: %s" % (latest_vid_loc))
				os.remove (latest_vid_loc)
			latest_vid_id = curr_vid_id
			latest_vid, latest_vid_loc = download_video(curr_vid_id)
		construct_image_dataset(latest_vid, curr_vid_id, curr_start_time, curr_end_time, curr_round_start, curr_round_end)
		# break
	logging.info("Finished generating the dataset!")


df = pd.read_csv(inputCsv)
generate_dataset(df)
