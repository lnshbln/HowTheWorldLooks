# -*- coding: utf-8 -*-
import json


out_file = open("/Volumes/Seagate Backup Plus Drive/thesis/images/Saint_Petersburg29_59_30_60/parsed_data.txt", 'w') # open output file
with open('/Volumes/Seagate Backup Plus Drive/thesis/images/Saint_Petersburg29_59_30_60/results1.json',"rb") as f: # replace "Your OWN JSON file.json" with your own JSON file
        file = f.readlines() # read all the lines in the JSON file
        for j in file:
          try:
            # Remove extra lines separating each tweet in the json file
            j = j.rstrip(','+'\n')
            #print(j)# j.rstrip('\n').rstrip().strip()
             # k is recording the number of lines processed
            if j:
                data = json.loads(j)  # Load the line into JSON format
                # extract the fields needed
                try:
                    idData = data["id"]
                    #user= data["realname"]
                    lat = data["latitude"]
                    lon = data["longitude"]
                    urls = data["url_l"]
                    main = str(urls[:30])
                    name = str(urls[30:])

                except KeyError:
                    urls = 'None'
                out_file.write(str(idData) + '\t' + str(lat) + '\t' + str(lon) + '\t' + str(urls) + '\n')
          except ValueError:
              continue
