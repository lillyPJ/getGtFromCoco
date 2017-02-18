#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# get gt_txt from the gt_json file
datasetDir='/home/lili/datasets/coco/raw'
dataType='train' # train/val
gtJson = '{}/gt/json/COCO_Text.json'.format(datasetDir)
imgDir = '{}/img/{}'.format(datasetDir, dataType)
txtDir = '{}/gt/{}/txt'.format(datasetDir, dataType)
# make txtDir
import os
if not os.path.exists(txtDir):
    os.makedirs(txtDir)

import coco_text
import re
import math
ct = coco_text.COCO_Text(gtJson)
if dataType == 'val':
    imgIdVal = ct.getImgIds(imgIds=ct.val)
elif dataType == 'train':
    imgIdVal = ct.getImgIds(imgIds=ct.train)
for num, eachId in enumerate(imgIdVal):

    # load img and anns
    img = ct.imgs[eachId]
    imgName = img['file_name']
    annId = ct.getAnnIds(imgIds=img['id'])
    anns = ct.loadAnns(annId)
    # precess box and tag
    bboxes = []
    tags = []
    for eachAnn in anns:
        bbox = [int(a) for a in eachAnn['bbox']]
        if(eachAnn['legibility'] == 'illegible'
           or not eachAnn.has_key('utf8_string')
           or eachAnn['language'] != 'english'):
            tag = '#'
        else:
            tag = eachAnn['utf8_string']
            tag = re.sub("\W+", "", tag)
        bboxes.append(bbox)
        tags.append(tag)
    # write to txt file
    txtFile = '{}/{}.txt'.format(txtDir, imgName[:-4])
    with open(txtFile, 'w') as f:
        if bboxes:
            for eachBox, eachTag in zip(bboxes, tags):
                f.write('{}, {}, {}, {}, "{}"\n'.format(eachBox[0], eachBox[1], eachBox[2] + eachBox[0] - 1,
                                                    eachBox[3] + eachBox[1] - 1, eachTag))
    # debug inform
    if not (num%500):
        print num