'''
python pred_video.py models/start_detector.oct_4.xgb drBfsroVfeo
'''
import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
sys.path.append("../utils/")
startModelFile = sys.argv[1]
vid_id = sys.argv[2]
from video_img_util import get_numpy_frames_for_video, load_image_from_array
import os
import numpy as np 
import xgboost as xgb 
import matplotlib.pyplot as plt


frames = get_numpy_frames_for_video(vid_id)
dval = xgb.DMatrix(frames)

startModel = xgb.Booster({'nthread':4})
startModel.load_model(startModelFile)

predictions = startModel.predict(dval)

# print predictions
# plt.plot(predictions)
# plt.show()

max_index = np.argmax(predictions)
max_frame = frames[max_index]
max_image = load_image_from_array(max_frame)
max_image.show()
