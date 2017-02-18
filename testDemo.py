
# dataset dir
datasetDir='/home/lili/datasets/coco/raw'
dataType='val'

gtJson = '{}/gt/json/COCO_Text.json'.format(datasetDir)
imgBaseDir = '{}/img'.format(datasetDir)
imgTrainDir = '{}/train'.format(imgBaseDir)
imgValDir = '{}/val'.format(imgBaseDir)

# load val imgs and show iamges, annotations
import coco_text
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab

ct = coco_text.COCO_Text(gtJson)
imgIdVal = ct.getImgIds(imgIds=ct.val, catIds=[('legibility','legible'),('class','machine printed')])
img = ct.loadImgs(imgIdVal[np.random.randint(0,len(imgIdVal))])[0]
annIds = ct.getAnnIds(imgIds=img['id'])
anns = ct.loadAnns(annIds)
I = io.imread('%s/img/%s/%s'%(datasetDir,dataType,img['file_name']))

print '/images/%s/%s'%(dataType,img['file_name'])
plt.figure()
plt.imshow(I)
ct.showAnns(anns)
plt.show()
print('ok')

