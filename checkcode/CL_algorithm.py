# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 19:36:37 2016

@author: Junfu Pu, pjh@mail.ustc.edu.cn

Algorithm for CaptchaLess
"""

import Image
import numpy as np
from os import listdir
import os
import scipy

class YJS_EPC:
    def __getTemplate_yjs(self):
        im1 = Image.open('Template_yjs_epc/0130')
        im2 = Image.open('Template_yjs_epc/3214')
        im3 = Image.open('Template_yjs_epc/7564')
        im4 = Image.open('Template_yjs_epc/7849')
        bw_im1 = np.array(im1.convert('L'))>128
        bw_im2 = np.array(im2.convert('L'))>128
        bw_im3 = np.array(im3.convert('L'))>128
        bw_im4 = np.array(im4.convert('L'))>128
        
        dic_0 = bw_im1[:,0:10].copy()
        dic_1 = bw_im1[:,10:20].copy()
        dic_2 = bw_im2[:,10:20].copy()
        dic_3 = bw_im2[:,0:10].copy()
        dic_4 = bw_im2[:,30:40].copy()
        dic_5 = bw_im3[:,10:20].copy()
        dic_6 = bw_im3[:,20:30].copy()
        dic_7 = bw_im3[:,0:10].copy()
        dic_8 = bw_im4[:,10:20].copy()
        dic_9 = bw_im4[:,30:40].copy() 
        Dict = [dic_0,dic_1,dic_2,dic_3,dic_4,dic_5,dic_6,dic_7,dic_8,dic_9]
        return Dict
    

    def makePrediction_yjs(self, img_test):
        Dict = self.__getTemplate_yjs()
        dist = np.zeros((10,4))
        img_test = np.array(img_test.convert('L'))>128
        for i in range(4):
            subImg = img_test[:,i*10:(i+1)*10]
            j = 0
            for dic in Dict:
                dist[j,i] = (dic^subImg).sum()
                j += 1   
        result = dist.argmin(axis=0)
        checkcode = ''.join([str(e) for e in result])
        return checkcode

class MIS:
    def __getTemplate_mis(self):
        Names_num = ['2.npy','3.npy','4.npy','5.npy','6.npy', \
                    '7.npy','8.npy','9.npy']
        Names_alp = []
        for i in range(65,91):
            Names_alp.append(chr(i)+'.npy')
        Names_alp.remove('I.npy')
        Dict = []
        label = []
        
        i = 2
        for name in Names_num:
            img = np.load('Template_mis4/'+name)
#            bw_img = np.array(img.convert('L'))>128
            bw_img = img            
            Dict.append(bw_img)
            label.append(str(i))
            i += 1
        
        for i in range(65,91):
            label.append(chr(i))
        label.remove('I')
        
        for name in Names_alp:
            img = np.load('Template_mis4/'+name)
#            bw_img = np.array(img.convert('L'))>128
            bw_img = img
            Dict.append(bw_img)    
        return (Dict,label)
     
    def makePrediction_mis(self, img_test):
        (Dict,label) = self.__getTemplate_mis()
        dist = np.zeros((33,4))
#        img_test = np.array(img_test.convert("L"))>128
        
        for i in range(4):
            subImage = img_test[i]
            j = 0
            for dict in Dict:
                d = (dict^subImage).sum()
#                d = np.zeros(10)
#                for k in range(10):
#                    subTemplate = dict[k:20+k,:]
#                    d[k] = (subTemplate^subImage).sum()
                dist[j,i] = d
                j += 1
        
        result_index = dist.argmin(axis=0)
        result = []
        for res in result_index:
            result.append(label[res])
        checkcode = ''.join([str(e) for e in result])
        return checkcode
        
    def makePrediction_mis_test(self, img_test):
        (Dict,label) = self.__getTemplate_mis()
        result = []        
        for i in range(4):
            subImg = img_test[i]
            result.append(self.makePrediction_mis_single(subImg, Dict, label))
        checkcode = ''.join(result)
        return checkcode
        
    def makePrediction_mis_single(self, subImage, Dict, label):
        testFeat = self.__getFeature(subImage)
        dist = np.zeros(33)
        for i in range(33):
            tempImg = Dict[i]
            tempFeat = self.__getFeature(tempImg)
            dist[i] = ((tempFeat-testFeat)**2).sum()
        result_index = dist.argmin()
        result = str(label[result_index])                       
        return result
    def __getFeature(self, img):
        nR = 5;
        nC = 4;
        (r, c) = img.shape
        deltaR = r/nR
        deltaC = c/nC
        hist = np.zeros((nR, nC))
        for i in range(nR):
            for j in range(nC):
                block = img[i*deltaR:(i+1)*deltaR, j*deltaC:(j+1)*deltaC]
                hist[i,j] = block.sum()
        feat = hist.reshape(nR*nC)
        feat = feat/(float(feat.sum())+1)  
        return feat              
        
        
    def get_narrowest(self, im_array):
        min_width = 20
        min_angle = 0
        im_standrad = None
        min_word_left = 0
        min_word_right = 20
    
        # rotate the image and get the smallest width,treat the image at that time as template
        for angle in range(-90, 90, 1):
    		#im_array is bool array, cannot convert to image directly
            im_array_int = im_array.astype(np.uint8) 
            im = Image.fromarray(im_array_int)
            im_tmp = np.array(im.rotate(angle).convert('L'))
    
            [width, word_left, word_right] = self.get_width(im_tmp)
            if (width < min_width):
                min_width = width
                min_angle = angle
                im_standrad = im_tmp
                min_word_left = word_left
                min_word_right = word_right
    
        return [im_standrad, min_width, min_angle, min_word_left, min_word_right];    

#    def generate_template(self, code_name, im_array):
#
#        [im_standrad, min_width, angle, min_word_left, min_word_right] = self.get_narrowest(im_array)
#    
#        # use an array of 30x20 to contain word
#        bg = np.zeros(shape=(30,20), dtype = np.bool)
#        bg.dtype= "bool_"
#        bg[5:25, (20 - min_width)/2-2:(20 - min_width)/2 + min_width+2] = im_standrad[0:20, min_word_left-2:min_word_right+2]
#        np.save("./codes_template/"+code_name, bg)
#        f=open(code_name+'.jpg', 'wb')
#        bg.dtype="int"
#        f.write(bg)
#        f.close()
    
    # get the width of word in image array
    def get_width(self, im_array):
        word_left = 0
        word_right = 20
    
        for x in range(0, 20):
            col_sum = im_array[:, x].sum()
            if col_sum > 0:
                # print('word begin:', x)
                word_left = x
                break
        for x in reversed(range(20)):
            col_sum = im_array[:, x].sum()
            if col_sum > 0:
                # print('word end:', x)
                word_right = x
                break
    
        return [word_right - word_left, word_left, word_right]
    
    def split_codes(self, checkcode):
        codes = []
        for i in range(4):
            box = [20*i, 0, 20*(i+1), 20]
            code = checkcode.crop(box)
            code_array = np.array(code.convert('L')) < 128
            [narrowest_code_array,a,b,c,d] = self.get_narrowest(code_array)
            codes.append(narrowest_code_array)
            #plt.imshow(narrowest_code_array, cmap="Greys")
            #plt.show()
        return codes
    
