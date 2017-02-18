import os
import re
import skimage.io as io
import shutil

def makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        if not os.path.isdir(dirname):
            raise


def getFileList(path, ext = '.jpg'):
    '''return the list of all the files(ext) in the path'''
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(ext)]

import matplotlib.pyplot as plt
def displayBoxes(boxes, color='r', lineWidth=2):
    currentAxis = plt.gca()
    for each in boxes:
        coords = (each[0], each[1]), each[2], each[3]
        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))

def checkAnns(anns, imgSize):
    imgH = imgSize[0]
    imgW = imgSize[1]
    if len(imgSize) < 3:
        return False
    nAnn = len(anns)
    if nAnn < 1:
        return False
    tags = [t['tag'] for t in anns]
    boxes = [t['bbox'] for t in anns]
    if '#' in tags:
        return False
    boxesArray = np.array(boxes)
    width = boxesArray[:,2]
    height = boxesArray[:,3]
    wIdx = width > 20
    hIdx = height > 15
    xmax = boxesArray[:,0] + boxesArray[:,2]
    ymax = boxesArray[:,1] + boxesArray[:,3]
    xMaxIdx = xmax < imgW
    yMaxIdx = ymax < imgH
    xMinIdx = boxesArray[:,0] > 0
    yMinIdx = boxesArray[:,1] > 0
    if sum(wIdx) + sum(hIdx) + sum(xMaxIdx) + sum(yMaxIdx) + sum(xMinIdx) + sum(yMinIdx) < 6 * nAnn:
        return False
    return True

import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
def showAnns(anns):
    """
    Display the specified annotations.
    :param anns (array of object): annotations to display
    :return: None
    """
    if len(anns) == 0:
        return 0
    ax = plt.gca()
    rectangles = []
    color = []
    for ann in anns:
        left, top, width, height = ann['bbox']
        rectangles.append(Rectangle([left,top],width,height,alpha=0.4))
        if 'tag' in ann.keys():
            ax.annotate(ann['tag'],(left,top-4), color=(0,0,1))
    p = PatchCollection(rectangles, edgecolors=(1,0,0), linewidths=3, alpha=0.4)
    ax.add_collection(p)

#-----------------------------------------
# dataset
rawDatasetDir = '/home/lili/datasets/coco/raw'
dataType = 'train'
imgDir = '{}/img/{}'.format(rawDatasetDir, dataType)
txtDir = '{}/gt/{}/txt'.format(rawDatasetDir, dataType)
figDir = '{}/fig/{}'.format(rawDatasetDir, dataType)
newDatasetDir = '/home/lili/datasets/coco'
newImgDir = '{}/img/{}'.format(newDatasetDir, dataType)
newTxtDir = '{}/gt/{}/txt'.format(newDatasetDir, dataType)

# make new dirs
makedirs(figDir)
makedirs(newImgDir)
makedirs(newTxtDir)

# get all gt_txt name
txtList = getFileList(txtDir, '.txt')
count = 0
allBoxes = []
for eachTxt in txtList:
    # read txt file
    gt = open(eachTxt).read().splitlines()
    anns = []
    for eachGt in gt:
        spt = re.split('[,]? ', eachGt)
        ann = {}
        ann['bbox'] = [int(a) for a in spt[:-1]]
        ann['bbox'][2] = ann['bbox'][2] - ann['bbox'][0]
        ann['bbox'][3] = ann['bbox'][3] - ann['bbox'][1]
        ann['tag'] = spt[4][1:-1]
        anns.append(ann)
    imgName = '{}/{}.jpg'.format(imgDir, os.path.basename(eachTxt)[:-4])
    img = io.imread(imgName)
    imgSize = img.shape
    # check the annotations
    if not checkAnns(anns, imgSize):
        continue
    # copy to the new dir
    imgName = os.path.splitext(os.path.basename(eachTxt))[0]
    sourceDir = '{}/{}.jpg'.format(imgDir, imgName)
    targetDir = '{}/{}.jpg'.format(newImgDir, imgName)
    shutil.copy(sourceDir, targetDir)
    sourceDir = eachTxt
    targetDir = '{}/{}'.format(newTxtDir, os.path.basename(eachTxt))
    shutil.copy(eachTxt, targetDir)
    count = count + 1
    print count
