from os import listdir
#import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np
import scipy

curr_path = os.path.dirname(os.path.abspath(__file__))
codes_path = os.path.join(curr_path, "codes2")
box = (0, 0, 25, 20)

# def preprocess_image()
def pad_to_center(im_array, col,row, center_left, center_right):
    w,h = im_array.size()
    bg = np.zeros(shape=(col, row), dtype = np.bool_)
    min_width = center_right - center_left
    bg[5:25, (20 - min_width)/2:(20 - min_width)/2 + min_width] = im_array[0:w, center_left:center_right]
    im_standrad = bg

def get_narrowest(im_array):
    w = im_array.shape
    w  = w[1]
#    assert False
    min_width = w
    min_angle = 0
    im_standrad = None
    min_word_left = 0
    min_word_right = w
    print('image width:', w)
    # rotate the image and get the smallest width,treat the image at that time as template
    for angle in range(-45, 45, 1):
        im_array_int = im_array.astype(np.uint8) #im_array is bool array, cannot convert to image directly
        im = Image.fromarray(im_array_int)
        im_tmp = np.array(im.rotate(angle).convert('L'))

        [width, word_left, word_right] = get_width(im_tmp)
        if (width < min_width):
            min_width = width
            min_angle = angle
            im_standrad = im_tmp
            min_word_left = word_left
            min_word_right = word_right

    print('left:', min_word_left)
    print('right:',min_word_right)
    bg = np.zeros(shape=(30,20), dtype = np.bool_)

    new_left = (20 - min_width) / 2
    new_right = new_left +min_width
    old_left = min_word_left
    old_right = old_left + min_width
    if new_right > 20:
        new_right = 20
        old_right = 20+old_left-new_left
    if old_right > w:
        old_right = w
        new_right = new_left + w - old_left
    print('new_left:', new_left)
    print('new_right:', new_right)
    print('old_left:', old_left)
    print('old_right:', old_right)
    bg_h, bg_w = bg.shape
    im_h,im_w = im_standrad.shape
    print('bg w:', bg_w)
    print('bg h:', bg_h)
    print('im_w:', im_w)
    print('im h:', im_h)
    print('old_right:', old_right)
    bg[5:25, new_left:new_right] = im_standrad[0:20, old_left: old_right]
    # a = bg[5:25, 8:23]
    # b = im_standrad[0:20, 8:23]
    # a_h,a_w = a.shape
    # b_h, b_w = b.shape
    # print('a_w', a_w)
    # print('b_w', b_w)
    #
    # bg[5:25, 8:23] = im_standrad[0:20, 8:23]
    # im_standrad = bg

    #plt.imshow(bg, cmap="Greys")
    #plt.show()

    return bg 

# code_name:'2','A',..
# im_array: binaried image arrays.
def generate_template(code_name, im_array):

    bg = get_narrowest(im_array)
    np.save("./codes2_template/"+code_name, bg)
    f=open(code_name+'.jpg', 'wb')
    bg = bg.astype(np.uint8)
    # bg.dtype="int"
    f.write(bg)
    f.close()

# get the width of word in image array
def get_width(im_array):
    h, w = im_array.shape
    word_left = 0
    word_right = w

    for x in range(0, w):
        col_sum = im_array[:, x].sum()
        if col_sum > 0 and word_left ==0:
            if x < 5:
                continue
            # print('word begin:', x)
            word_left = x
            break
        if col_sum == 0 and x < 10 and word_left != 0:
            word_left = 0

    for x in reversed(range(w)):
        col_sum = im_array[:, x].sum()
        if col_sum > 0:
            # print('word end:', x)
            word_right = x
            break

    return [word_right - word_left, word_left, word_right]

def get_split_line(checkcode):
    code_array = np.array(checkcode.convert('L')) < 128
    split_lines = [0,]

    for i in range(0,3):
        left = 0
        right = 0
        for x in range(15+20*i, 30+20*i):
            curr_line_sum = code_array[:, x].sum()
            if curr_line_sum == 0 and left==0:
                left = x
            if curr_line_sum != 0 and left != 0:
                right = x
                break
            if right == 0:
                right = 30+20*i
        # print('split left:',left)
        # print('split right:',right)
        print('split :',(right+left)/2)
        split_lines.append((left+right)/2)

    split_lines.append(80)
    return split_lines;

def split_codes(checkcode):
    codes = []
    split_lines = get_split_line(checkcode)
    for i in range(4):
        box = [split_lines[i], 0, split_lines[i+1], 20]
        code = checkcode.crop(box)

        code_array = np.array(code.convert('L')) < 128
        #plt.imshow(code_array, cmap="Greys")
        #plt.show()
        print(code_array)
        narrowest_code_array = get_narrowest(code_array)
        codes.append(narrowest_code_array)

    return codes

#file_list = listdir(codes_path)
#for file in file_list:
#    code_name = file[0]
#    print('code_name:' + code_name)
#    im = Image.open(os.path.join(codes_path, file))
#    im = im.crop(box)
#    im_array = np.array(im.convert('L')) < 128
#    print(im_array)
#    #plt.imshow(im_array, cmap="Greys")
#    #plt.show()
#    generate_template(code_name, im_array)
#    # split_codes(im)
#    # im2 = np.load('./templates_npy/O.npy')
#    # im2_int = im2.astype(np.uint8)
#    # plt.imshow(im2, cmap="Greys")
#    # plt.show()
#
#im = Image.open("code.jpg")
#
# im.rotate(10).show()
