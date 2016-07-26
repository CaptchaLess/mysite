import cv2
from PIL import Image
import os
from skimage.feature import local_binary_pattern
from scipy.stats import itemfreq
from sklearn.preprocessing import normalize
import numpy as np
import cvutils
import csv
import cPickle

def get_split_line():
    split_lines = [3,23,43,63,80]
    return split_lines

def span_array(array):
	for i in range(26):
		if i not in array[:,0]:
			array = np.append(array, [[i, 0]], axis=0)		
			array = np.sort(array, axis=0)
	return array

def calculate_hist(im):
	im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	tmp,im_binary = cv2.threshold(im_gray,  128, 255, cv2.THRESH_BINARY)	
	radius = 3
	num_points = 8 * radius
	lbp = local_binary_pattern(im_binary, num_points, radius, method='uniform')
	x = itemfreq(lbp.ravel())
#	print(x.shape)
	if x.shape[0] != 26:
		x = span_array(x)

	if x.shape[0] < 20:
		print(x)
		print(x.shape)
	hist = x[:,1] / sum(x[:,1])
	return hist

def train_save(train_set_path):
	train_hist = []
	train_name = []
	
	train_images = cvutils.imlist(train_set_path)
	for ti in train_images:
		im = cv2.imread(ti)
		hist = calculate_hist(im)	
		train_name.append(ti)
		train_hist.append(hist)
	cPickle.dump(train_name, open('train_name.p', 'wb'))	
	cPickle.dump(train_hist, open('train_hist.p', 'wb'))	
	
	return train_name, train_hist

def train_load():
	train_name = cPickle.load(open('train_name.p','rb'))
	train_hist = cPickle.load(open('train_hist.p','rb'))
	return train_name, train_hist	

def test(im, train_set_path):
	split_lines = get_split_line()
	results = []
	if os.path.isfile('train_name.p'):
		train_name, train_hist = train_load()
	else:
		train_name, train_hist = train_save(train_set_path)
	for i in range(4):
		box = [split_lines[i], 0, split_lines[i+1], 20]
		curr_im = im.crop(box)

		im_rgb = curr_im.convert("RGB")
		im_rgb.save('tmp.jpg', 'JPEG')
		im_rgb = cv2.imread('tmp.jpg')
		results.append(test_each_code(im_rgb, train_name, train_hist))

	return ''.join(results)

def test_each_code(curr_im, train_name, train_hist):
	test_hist = calculate_hist(curr_im)
	results = []
	for index, train_hist in enumerate(train_hist):
		score = cv2.compareHist(np.array(train_hist, dtype=np.float32), \
		np.array(test_hist, dtype=np.float32),cv2.cv.CV_COMP_CHISQR)
		results.append((train_name[index], round(score,3)))
		
#	print('==============')
	results = sorted(results, key=lambda score: score[1])
#	print(results[0:20])
#	print(results[0][0])
	
	label = results[0][0].split('/')[-1].split('.')[0].split('-')[0]	
#	print('label:',label)
	
	return label

if __name__ == '__main__':
	test_checkcodes = cvutils.imlist('./test_checkcode/')
	time = 0
	accu = 0
	for file in test_checkcodes:
		time  = time + 1
		print('checkcode:',file)
		im = Image.open(file)
		result = test(im, './template_rgb/')
		print('result:', result)	
		if result == file.split('/')[-1].split('.')[0]:
			accu = accu + 1
		else:
			print('error!', time - accu)
			

	print('accuracy:%d / %d = %f'%(accu, time, float(accu)/ time))	
		
