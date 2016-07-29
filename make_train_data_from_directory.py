#!/usr/bin/env python
# encoding:utf-8

# discription:
#
# generate dataset text data such as train.txt, test.txt, and label.txt for learning images
#
# waring: jpg only
#
import sys
import commands
import subprocess
import glob
import os
import shutil
import argparse
import random

def getdirs(path):
    dirs=[]
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path,item)):
            dirs.append(item)
    return dirs

parser = argparse.ArgumentParser(description='script for generating dataset text')
parser.add_argument('src_path', help= "directry root path")
parser.add_argument('-l', '--limit', help= 'maximum number of photo in each class')
args = parser.parse_args()


#labels
dirs = getdirs(args.src_path)
print dirs
labels = dirs[:]

#make directries
if not os.path.exists(args.src_path + "/images") :
    os.mkdir(args.src_path + "/images")

#copy images and make train.txt
imageDir = args.src_path +"/images"
train     = open( args.src_path + 'train.txt','w')
test      = open( args.src_path + 'test.txt','w')
labelsTxt = open( args.src_path + 'labels.txt','w')
resize    = open( args.src_path + 'resize.txt','w') 

classNo=0
cnt = 0
#label = labels[classNo]
for label in labels:
	workdir = args.src_path + label
	images = glob.glob(workdir + '/*.jpg')
	print(label)
	labelsTxt.write(label+"\n")
	startCnt=cnt
        if (args.limit):
	    length = int(args.limit)
	else:
	    length = len(images)
        prob = float(length) / float(len(images))
        print "prob=" +  str(prob)

	for image in images:
            if (prob < 1.0 and random.random() >= prob):
                continue
            savepath = imageDir+"/image%07d" %cnt +".jpg"
            shortpath =  "images/image%07d" %cnt +".jpg" 
            shutil.copyfile(image, savepath)
	    if cnt-startCnt < length*0.75:
		train.write(shortpath+" %d\n" % classNo)
	    else:
		test.write(shortpath+" %d\n" % classNo)
            resize.write(shortpath+" %d\n" % classNo)
            cnt += 1
	
	classNo += 1

train.close()
test.close()
labelsTxt.close()
