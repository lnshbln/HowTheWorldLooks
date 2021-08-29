
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
    groups = [170]
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

        j = i
        return (color)



def adoptiveColorExtraction():

    newMass = []
    editedMass = []
    k =0
    for i in range(0, len(n)):
                if n[i]>=approxNumberOfColor:
                    if (b[i]-k)>30:
                        k = b[i]
                        newMass.append(b[i])
                        color = GreyToRGB(b[i])
                        editedMass.append(color)
                    else:
                        continue







keywords = []
lat = []
lon = []
ExtractedColor = []
with open('fullpathtocitiescodes.txt') as csv_file:  # open vocabulary file

    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        keywords.append(row[0])
        lat.append(row[1])
        lon.append(row[2])

urls = []
for keyword in keywords:

    try:

        rgb_weights = [0.2989, 0.5870, 0.1140]
        #rgb_weights = [0.24, 0.2600, 0.25]
        url = '/photos/'+keyword+'/architecture/*.jpg'
        img = mpimg.imread(url)
        urls.append(url)
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

        newColor = threeMainColors(n,b,SummMatrix,RWeightedmatrix,GWeightedmatrix,BWeightedmatrix,rgb_weights)
        ExtractedColor.append(newColor)

    except AttributeError:
        continue
    except IOError:
        continue

rows = zip(keywords, lat, lon,ExtractedColor,urls)

out_file = open('outputfile.txt', 'w')  # open output file
writer = csv.writer((out_file), delimiter='\t')
for row in rows:
        writer.writerow(row)
