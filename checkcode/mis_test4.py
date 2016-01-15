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

def get_narrowest(im_array):
    min_width = 20
    min_angle = 0
    im_standrad = None
    min_word_left = 0
    min_word_right = 20

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

    return [im_standrad, min_width, min_angle, min_word_left, min_word_right];

# code_name:'2','A',..
# im_array: binaried image arrays.
def generate_template(code_name, im_array):

    [im_standrad, min_width, angle, min_word_left, min_word_right] = get_narrowest(im_array)

    # use an array of 30x20 to contain word
    bg = np.zeros(shape=(30,20), dtype = np.bool_)
    # bg.dtype= "bool_"
    bg[5:25, (20 - min_width)/2-2:(20 - min_width)/2 + min_width+4] = im_standrad[0:20, min_word_left-2:min_word_right+4]
    # plt.imshow(bg, cmap="Greys")
    # plt.show()
    np.save("./codes2_template/"+code_name, bg)
    f=open(code_name+'.jpg', 'wb')
    bg = bg.astype(np.uint8)
    # bg.dtype="int"
    f.write(bg)
    f.close()

# get the width of word in image array
def get_width(im_array):

    word_left = 0
    word_right = 20

    for x in range(0, 20):
        col_sum = im_array[:, x].sum()
        if col_sum > 0 and word_left ==0:
            if x < 5:
                continue
            # print('word begin:', x)
            word_left = x
            break
        if col_sum == 0 and x < 10 and word_left != 0:
            word_left = 0

    for x in reversed(range(20)):
        col_sum = im_array[:, x].sum()
        if col_sum > 0:

            # print('word end:', x)
            word_right = x
            break

    return [word_right - word_left, word_left, word_right]

def split_codes(checkcode):
    codes = []
    for i in range(4):
        box = [20*i, 0, 20*(i+1)+2, 20]
        code = checkcode.crop(box)

        code_array = np.array(code.convert('L')) < 128
        #plt.imshow(code_array, cmap="Greys")
        #plt.show()
        [narrowest_code_array,min_width, angle, min_word_left, min_word_right] = get_narrowest(code_array)
        print('min_width:',min_width)
        print('left:',min_word_left)
        print('right:',min_word_right)

        # [im_standrad, min_width, angle, min_word_left, min_word_rtigh] = get_narrowest(im_array)

        # use an array of 30x20 to contain word
        bg = np.zeros(shape=(30,20), dtype = np.bool_)
        # bg.dtype= "bool_"
        bg[5:25, (20 - min_width)/2-2:(20 - min_width)/2 + min_width+2] = narrowest_code_array[0:20, min_word_left-2:min_word_right+2]
        narrowest_code_array = bg
        codes.append(narrowest_code_array)
        #plt.imshow(narrowest_code_array, cmap="Greys")
        #plt.show()
    return codes

#file_list = listdir(codes_path)
#for file in file_list:
#    code_name = file[0]
#    print('code_name:' + code_name)
#    im = Image.open(os.path.join(codes_path, file))
#    # im = im.crop(box)
#    # im_array = np.array(im.convert('L')) < 128
#    # print(im_array)
#    # plt.imshow(im_array, cmap="Greys")
#    # plt.show()
#    # generate_template(code_name, im_array)
#    split_codes(im)
#    # im2 = np.load('./templates_npy/O.npy')
#    # im2_int = im2.astype(np.uint8)
#    # plt.imshow(im2, cmap="Greys")
#    # plt.show()
#
#im = Image.open("code.jpg")
#
# im.rotate(10).show()
