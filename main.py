# python 3.9 here
# script for orchestrateing the emotional system. DP processing and bahavior changes


import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time
import json
from datetime import date

from multimodalDLforER.processor import Processor
from argparse import Namespace

today = date.today().strftime("%b-%d-%Y")

args = Namespace(configuration='multimodalDLforER/configs/embracenet_plus.json',
				cuda=0, dataset=None, inputfile='siu.jpg',
				modality=None, mode='inference',
				multimodel='multimodalDLforER/checkpoints/checkpoints/ebnplus/allmerge_ebnp.pth',
				oversample=False, pretrained=True, savename=None,
				threshold='multimodalDLforER/checkpoints/thresholds/thresholds_validation.npy',
				unimodal=False, unimodel=None, unimodels='multimodalDLforER/checkpoints/models/')
P = Processor(args)

emotions = {'joy':2, 'trust': 2,
			'anticipation': 1, 'surprise' :1,
			'sadness':-1, 'fear':-1,
			'anger':-2, 'disgust': -2}

def evaluate_emotions(results):
	emotional_value = 0
	print(results)
	for idx in range(results['total']):
		d_emos = results[str(idx)]['emotions']
		print(idx, d_emos)
		for e in d_emos:
			emotional_value += emotions[e]

	print('Emotional value:' , emotional_value)
	os.system('python2 change_behaviour.py --emovalue '+ str(emotional_value))

def process_image(image, emotion=True, size=(224,224)):

	P.Inputfile = image
	P.Inputname = image[9:-4]

	t0 = time.time()
	P.start()
	t1 = time.time()

	print ("processing time ", t1 - t0)

	with open('results_'+P.Inputname+'.json') as json_res:
		results = json.load(json_res)
		
		evaluate_emotions(results)

if __name__ == '__main__':

	count = 0

	while True:
		os.system('python2 pp2p2.py --name '+today +'_'+str(count))
		try:
			process_image('captures/'+today +'_'+ str(count)+'.png')
			count += 1
			#time.sleep(1)
		except:
			print('Error')
			break
		if count==6:
			break

	