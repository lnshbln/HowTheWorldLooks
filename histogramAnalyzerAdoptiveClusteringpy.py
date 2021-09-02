
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import scipy.signal as signal
import matplotlib
from colour import Color
import csv

import scipy.misc
import scipy.ndimage

def GreyToRGB (b,SummMatrix,RWeightedmatrix,GWeightedmatrix,BWeightedmatrix,rgb_weights):
  try:
        bnew = round(b)
        redZip = zip(SummMatrix,RWeightedmatrix)
        greenZip = zip(SummMatrix,GWeightedmatrix)
        blueZip = zip(SummMatrix,BWeightedmatrix)
        for i,y, in(redZip):
            k1 = 0
            for j,u in zip(i,y):
                if round(j) == bnew:
                    k1 = u
                    break
        for i,y, in(greenZip):
            k2 = 0
            for j,u in zip(i,y):
                if round(j) == bnew:
                    k2 = u
                    break
        for i,y, in(blueZip):
            k3 = 0
            for j,u in zip(i,y):
                if round(j) == bnew:
                    k3 = u
                    break
        R = (b *k1/rgb_weights[0])/255
        if R>1:
            R =1
        G = (b *k2/rgb_weights[1])/255
        if G>1:
            G =1
        B = (b *k3/rgb_weights[2])/255
        if B>1:
            B =1
        newColor = (R,G,B)
        c = Color(rgb=newColor)
        if c  != Color('black'):
            return(c)

  except TypeError:
            print(1)



def threeMainColors(n,b,SummMatrix,RWeightedmatrix,GWeightedmatrix,BWeightedmatrix,rgb_weights):
    j = 0
    k= 0
    newMass = []
    groups = [40,80,120,150,180,220]
    editedColor = []
    extractedColor = []
    for i in groups:
        for l in range(k,i):
            newMass.append(n[l])
        amax = np.max(newMass)
        k = i
        for y in range(j,i):
            if j == i:
                break
            elem = n[y]
            value = b[y]
            if elem == amax:
                break
            else:  # ideally this should never be tripped
                y = None

        color = GreyToRGB(value,SummMatrix,RWeightedmatrix,GWeightedmatrix,BWeightedmatrix,rgb_weights)
        editedColor.append(color)
        extractedColor.append(int(value))
        j = i

    return (editedColor,extractedColor)



def adoptiveColorExtraction(n,b,SummMatrix,RWeightedmatrix,GWeightedmatrix,BWeightedmatrix,rgb_weights,approxNumberOfColor):
  try:
    newMass = []
    editedMass = []
    k =0
    Smatrix = SummMatrix
    RWeigts = RWeightedmatrix
    GWeights = GWeightedmatrix
    BWeights = BWeightedmatrix
    RGBW = rgb_weights
    for i in range(0, len(n)):
         if n[i]>=approxNumberOfColor:
                    if (b[i]-k)>30:
                        k = b[i]
                        newMass.append(b[i])

                        print (k)
                    else:
                        continue

         color = GreyToRGB(k, Smatrix, RWeigts, GWeights, BWeights, RGBW)
         editedMass.append(color)
         return (editedMass)
  except TypeError:
            print(1)





keywords = []
lat = []
lon = []
ExtractedColor = []
CodedColor = []
urlsInt = []
with open('/Volumes/Seagate Backup Plus Drive/thesis/images/New_York_City-74.27_40.49_-73.66_40.93/parsed_data.txt') as csv_file:  # open vocabulary file

    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        keywords.append(row[0])
        lat.append(row[1])
        lon.append(row[2])
        urlsInt.append(row[3])

urls = []
for keyword in keywords:

    try:

        rgb_weights = [0.2989, 0.5870, 0.1140]
        #rgb_weights = [0.24, 0.2600, 0.25]
        url = '/Volumes/Seagate Backup Plus Drive/thesis/images/New_York_City-74.27_40.49_-73.66_40.93/'+keyword+'.jpg'
        img = mpimg.imread(url)
        urls.append(url)
        #scipy.ndimage.imread('/Users/elena/Sentinel_processing/000018.jpg', mode='L')
        #scipy.misc.face()
        size = img.size
        approxNumberOfColor = size*0.0001

        grayimg = np.dot(img[...,:3], rgb_weights)

        n,b,c = plt.hist(grayimg.ravel(),254,[1,254])


        # Convert the image
        R = img[..., 0]
        G = img[..., 1]
        B = img[..., 2]

        Rtransform = np.asarray(R *rgb_weights[0])
        Gtransform = np.asarray(G *rgb_weights[1])
        Btransform = np.asarray(B *rgb_weights[2])
        SummMatrix = (Rtransform+Gtransform+Btransform)
        RWeightedmatrix = (Rtransform/SummMatrix)
        GWeightedmatrix = (Gtransform/SummMatrix)
        BWeightedmatrix = (Btransform/SummMatrix)

        newColor,codeColor = threeMainColors(n,b,SummMatrix,RWeightedmatrix,GWeightedmatrix,BWeightedmatrix,rgb_weights)

        ExtractedColor.append(newColor)
        CodedColor.append(codeColor)

    except AttributeError:
        continue
    except IOError:
        continue

rows = zip(keywords, lat, lon,ExtractedColor,CodedColor,urls)

out_file = open('/Volumes/Seagate Backup Plus Drive/thesis/images/Saint_Petersburg29_59_30_60/colors2.txt', 'w')  # open output file
writer = csv.writer((out_file), delimiter='\t')
for row in rows:
        writer.writerow(row)



#bin_max = np.where(a == a.max())

#print ('maxbin', b[bin_max][0])
#print (n,b)
"""
a = np.max(n)
print(a)
for y in range(0,len(n)):
    elem = n[y]
    if elem == a:
     break
else:   # ideally this should never be tripped
    y = None
print b[y]
"""


"""

for i in newMass:
    if (i-k)>10:
        color = GreyToRGB(i)
        editedMass.append(i)
        k = i
    else:
        continue

print(editedMass)
"""