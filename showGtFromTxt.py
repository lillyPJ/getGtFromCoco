
# dataset
datasetDir = '/home/lili/datasets/coco'
dataType = 'val'
imgDir = '{}/img/{}'.format(datasetDir, dataType)
txtDir = '{}/gt/{}/txt'.format(datasetDir, dataType)
figDir = '{}/fig/{}'.format(datasetDir, dataType)


import os
import re
import skimage.io as io


if not os.path.exists(figDir):
    os.makedirs(figDir)

def getFileList(path, ext = '.jpg'):
    '''return the list of all the files(ext) in the path'''
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(ext)]

import matplotlib.pyplot as plt
def displayBoxes(boxes, color='r', lineWidth=2):
    currentAxis = plt.gca()
    for each in boxes:
        coords = (each[0], each[1]), each[2], each[3]
        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))

def checkAnns(anns):
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
    if sum(wIdx) + sum(hIdx) < 2 * nAnn:
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
# ---------------show all images and annotations_box--------------
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

    # # load and show image
    imgName = '{}/{}.jpg'.format(imgDir, os.path.basename(eachTxt)[:-4])
    img = io.imread(imgName)
    plt.figure()
    plt.imshow(img)
    # show bounding box
    showAnns(anns)
    print('{}:{}\n',imgName, len(anns))
    #plt.show()
    plt.savefig('{}/{}.jpg'.format(figDir, os.path.basename(eachTxt)[:-4]))
    count = count + 1
print count
