# python 3.9 here
# script for orchestrating the emotional system. DP processing and behavior changes


import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time
import json
from datetime import date

from multimodalDLforER.processor import Processor
from argparse import Namespace

'''
today : String used to name captured images, sending to face_recognition.py script
args : Namespace with all needed variables in multimodalDLforER.processor instance. The namespace form makes easy the Processor usage
* note that default configurations follows the multimodalDLforER github guidance
'''

today = date.today().strftime("%b-%d-%Y")

args = Namespace(configuration='multimodalDLforER/configs/embracenet_plus.json',
			cuda=0, dataset=None, inputfile='siu.jpg',
			modality=None, mode='inference',
			multimodel='multimodalDLforER/checkpoints/checkpoints/ebnplus/allmerge_ebnp.pth',
			oversample=False, pretrained=True, savename=None,
			threshold='multimodalDLforER/checkpoints/thresholds/thresholds_validation.npy',
			unimodal=False, unimodel=None, unimodels='multimodalDLforER/checkpoints/models/')
P = Processor(args)

'''
emotions : Dictionary with the possible recognised emotions and their respective score, following the positivity and negativity of each emotion.
'''
emotions = {'joy':2, 'trust': 2,
		'anticipation': 1, 'surprise' :1,
		'sadness':-1, 'fear':-1,
		'anger':-2, 'disgust': -2}

def evaluate_emotions(results):
	'''
	IN  results : dictionary with results from DL model
	'''
	emotional_value = 0
	# print(results)
	for idx in range(results['total']):
		d_emos = results[str(idx)]['emotions'] # Getting the recognized emotions from 'idx' person
		# print(idx, d_emos)
		for e in d_emos:
			emotional_value += emotions[e] # Adding the related emotion scores

	print('Emotional value:' , emotional_value)
	os.system('python2 change_behaviour.py --emovalue '+ str(emotional_value)) # Calling change_behaviour script, passing the emotional value as parameter

def process_image(image, emotion=True, size=(224,224)):
	'''
	IN  image : the captured image path string
		emotion : emotions existence indicator bool
		size : pair with wxh dimension default values
	'''
	P.Inputfile = image
	P.Inputname = image[9:-4] # name of image by taking only the name without contained folder and extension

	t0 = time.time()
	P.start() # Function that execute the DL procedure and write the results
	t1 = time.time()

	print ("processing time ", t1 - t0)

	with open('results_'+P.Inputname+'.json') as json_res: # Open the result json with its default name
		results = json.load(json_res)
		
		evaluate_emotions(results)

if __name__ == '__main__':

	max_steps = 10
	count = 0

	while True:
		os.system('python2 face_recognition.py --name '+today +'_'+str(count))
		#os.system('python2 image_capturing.py --name '+today +'_'+str(count))
		try:
			process_image('captures/'+today +'_'+ str(count)+'.png')
			count += 1
		except:
			print('Error')
			break
		if count==max_steps:
			break