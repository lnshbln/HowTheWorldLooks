import csv

keywords = []
lat = []
lon = []
color = []
urls = []
with open('colors.txt') as csv_file:  # open vocabulary file

    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        keywords.append(row[0])
        lat.append(row[1])
        lon.append(row[2])
        color.append(row[3])
        urls.append(row[4])

file1 = open("myfile.txt","w")
for i,j,k,c,url in zip(keywords,lat,lon,color,urls):
    file1.write('{'+'"keyword":'+'"'+i+'"'+',"lat":'+'"'+j+'"'+',"lon":'+'"'+k+'"'+',"color":'+'"'+c+'"'+','+'"media":'+'"'+url+'"'+'},'+'\n')
