#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  crop pistures from imagenet style list (eg. hoge/hoge/test.jpg 2)
#
#  usage: ./crop_csv.py list_path destination_directory_path
#
import cv2
import argparse
import os
import numpy
import csv
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("list_file")
parser.add_argument("target_dir")
parser.add_argument('--root', '-r', default='',  help='Root directory path of image files')
parser.add_argument('--size', '-s', default=256, help='Root directory path of image files')

args = parser.parse_args()

target_shape = (args.size, args.size)

# ファイルパスを配列に入れて返す
def load_image_list(path):
    file_list = []
    for line in open(path, 'r'):
        vals = line.strip().split(' ')
        file_list.append(vals[0])
        print vals[0]
    return file_list

image_list = load_image_list(args.list_file)

for image in image_list:
    source_imgpath = image
    src = cv2.imread(args.root + source_imgpath)
    if (src == None) :
	print "fail"
	continue
    # resize image
    height, width, depth = src.shape
    new_height = target_shape[1]
    new_width = target_shape[0]
    if height > width:
        new_height = target_shape[1] * height / width
    else:
        new_width = target_shape[0] * width / height
    resized_img = cv2.resize(src, (new_width, new_height))
    height_offset = (new_height - target_shape[1]) / 2
    width_offset = (new_width - target_shape[0]) / 2
    cropped_img = resized_img[height_offset:height_offset + target_shape[1],
                                            width_offset:width_offset + target_shape[0]]
    if os.path.isdir(args.target_dir) == False :
	os.makedirs(args.target_dir)
    cv2.imwrite(args.target_dir+"/"+ os.path.basename(source_imgpath), cropped_img)
    print(args.target_dir+"/"+ os.path.basename(source_imgpath))
