# testing use of python 2 and 3
# python 3.4 here

import subprocess
import numpy as np
import matplotlib.pyplot as plt
import cv2

def process_image(image, emotion=True, size=(224,224)):
	image = cv2.resize(image, size)
	print(image.shape)
	# image = np.transpose(image,(2,0,1))
	if emotion:
		prediction = 0
		return (prediction, image)
	return image

if __name__ == '__main__':

	script = ["python2.7", "pp2p.py"]    
	process = subprocess.Popen(" ".join(script), shell=True, env={"PYTHONPATH": "."})
	
	while True:
		try:
			img = cv2.imread('camImage.png')
			break
		except:
			print('no image yet')
	
	print(img.shape)
	
