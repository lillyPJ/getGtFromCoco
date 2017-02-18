# dataset dir
datasetDir='/home/lili/datasets/coco/raw'
dataType='val2014'

gtJson = '{}/annotations/COCO_Text.json'.format(datasetDir)
gtJsonNew = '{}/annotations/COCO_Text_New.json'.format(datasetDir)
imgBaseDir = '{}/images'.format(datasetDir)
imgSourceDir = '{}/trainValAll'.format(imgBaseDir)
imgDestTrainDir = '{}/train'.format(imgBaseDir)
imgDestValDir = '{}/val'.format(imgBaseDir)

# load gt json file

# import json
# with open(gtJson) as json_file:
#     coco_text = json.load(json_file)

#--------------rectify the file_name of the imgs in 'val'--------
# import coco_text
# ct = coco_text.COCO_Text(gtJson)
# imgIds = ct.getImgIds(imgIds = ct.val)
# ct.changeImgNames(imgIds)
# import json
# with open(gtJsonNew, 'w') as jsonFile:
#     json.dump(ct.dataset, jsonFile)
# print 'ok!'

#-------------create the new dir for the coco-text image ------------
import coco_text
import os
import shutil
ct = coco_text.COCO_Text(gtJson)
imgIdVal = ct.getImgIds(imgIds=ct.val)
if not os.path.exists(imgDestValDir):
    os.mkdir(imgDestValDir)
for num, eachId in enumerate(imgIdVal):
    imgName = ct.imgs[eachId]['file_name']
    sourceDir = '{}/{}'.format(imgSourceDir, imgName)
    targetDir = '{}/{}'.format(imgDestValDir, imgName)
    shutil.copy(sourceDir, targetDir)
    if not (num%500):
        print num

imgIdTrain = ct.getImgIds(imgIds=ct.train)
if not os.path.exists(imgDestTrainDir):
    os.mkdir(imgDestTrainDir)
for num, eachId in enumerate(imgIdTrain):
    imgName = ct.imgs[eachId]['file_name']
    sourceDir = '{}/{}'.format(imgSourceDir, imgName)
    targetDir = '{}/{}'.format(imgDestTrainDir, imgName)
    shutil.copy(sourceDir, targetDir)
    if not (num%500):
        print num
