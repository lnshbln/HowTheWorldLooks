import csv

keywords = []
lat = []
lon = []

urls = []
extractedColors = []
codedColors = []
with open('/Users/elena/Documents/thesis/prototype/updatedVersion/2 2/colors1.txt') as csv_file:  # open vocabulary file

    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        keywords.append(row[0])
        lat.append(row[1])
        lon.append(row[2])
        extractedColors.append(row[3])
        codedColors.append(row[4])
        urls.append(row[5])


print(codedColors)
file1 = open("/Users/elena/Documents/thesis/prototype/updatedVersion/2 2/myfile.txt","w")
k1 = 0
k2 = 0
k3 = 0
k4 = 0
k5 = 0
w1 = 0
w2 = 0
w3 = 0
w4 = 0
w5 = 0
for i,j,k,c,p,url in zip(keywords,lat,lon,extractedColors,codedColors,urls):
    a = c.split(',')
    b = (p.split(','))
    print(b)
    for o,w in zip(a,b):
        print(w)
        if k1 == 0 and w1 == 0:
            k1 = o
            w1 = w
            continue
        elif k2 == 0 and w2 == 0:
            k2 = o
            w2 = w
            continue
        elif k3 == 0 and w3 ==0:
            k3 = o
            w3 = w
            continue
        elif k4 == 0 and w4 == 0:
            k4 = o
            w4 = w
            continue
        elif k5 == 0 and w5 ==0:
            k5 = o
            w5 = w
        else:
            continue

    print(k1,k2,k3,k4,k5,w1,w2,w3,w4,w5)

    file1.write('{'+'"keyword":'+'"'+i+'"'+',"lat":'+'"'+j+'"'+',"lon":'+'"'+k+'"'+',"color1":'+'"'+k1+'"'+',"color2":'+'"'+k2+'"'+',"color3":'+'"'+k3+'"'+',"color4":'+'"'+k4+'"'+',"color5":'+'"'+k5+'"'+',"coded1":'+'"'+w1+'"'+',"coded2":'+'"'+w2+'"'+',"coded3":'+'"'+w3+'"'+',"coded4":'+'"'+w4+'"'+',"coded5":'+'"'+w5+'"'+',"media":'+'"'+url+'"'+'},'+'\n')
    k1, k2, k3, k4, k5, w1, w2, w3, w4, w5 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0