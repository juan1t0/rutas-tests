# testing use of python 2 and 3
# python 3.4 here

#import subprocess
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time
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

def process_image(image, emotion=True, size=(224,224)):
	#image = cv2.resize(image, size)
	P.Inputfile = image
	print('a')
	P.start()
	print('b')
	#print(image.shape)
	# image = np.transpose(image,(2,0,1))
	with open('results'+image[-4]) as f:
		lines = f.readlines()
		print(lines)

if __name__ == '__main__':

	#script = ["python2", "pp2p.py"]    
	#process = subprocess.Popen(" ".join(script), shell=True)#, env={"PYTHONPATH": "."})
	count = 0

	while True:
		os.system('python2 pp2p.py --name '+today +'_'+str(count))
		try:
			#img = cv2.imread('captures/'+today +'_'+ str(count)+'.png')
			#print(img.shape)
			process_image('captures/'+today +'_'+ str(count)+'.png')
			count += 1
			time.sleep(5)
		except:
			print('error')
			break
		if count==11:
			break
	
	#print(img.shape)
	#plt.imshow(img)
	#plt.show()
	
