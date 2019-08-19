##code for scraping Haryana assembly elections Who's Who's data
##Mukul

import pdftotext
import pandas as pd
import re
from autocorrect import spell
import inflect
import os
all_files = os.listdir()
p = inflect.engine()

all_files = [i for i in all_files if i[-3:]=="pdf"]
all_files.sort()


for file in all_files:
    print("Scraping file " + file + " in process....")
    
    year = file[-8:-4]

    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f)

    data = []
    for i in range(len(pdf)):
        data.append(pdf[i])

    for i in range(len(data)):
        data[i] = data[i].split("\n")

    for i in data:
        for j in range(len(i)):
            i[j] = i[j].strip()
    start_page = 0
    end_page = 0

    for i in range(len(data)):
        if data[i][0]=="Biographical Sketches":
            start_page = i
        if len(data[i][0].split())!=0:

            if data[i][0].split()[0].lower()=="index":
                end_page = i

    def if_nearly_equal(a,b):

        a = a.lower()
        b = b.lower()
        a = re.sub('[^A-Za-z0-9]+', ' ', a)
        b = re.sub('[^A-Za-z0-9]+', ' ', b)

        a = a.split()
        b = b.split()
        la = len(a)
        lb = len(b)

        a = [spell(i) for i in a]
        b = [spell(i) for i in b]


        ca = 0
        cb = 0
        for i in a:
            if i in b:
                ca+=1
        for i in b:
            if i in a:
                cb+=1
        if (la+lb-ca-cb) < 5 and ca>=1 and cb>=1 and la==lb:
            return True
        else:
            return False



    def find_suitable(D,b):
        for i in D.keys():

            if if_nearly_equal(i,b):
                return i

        else :
            return -1



    countx = 0
    main = []
    each = []

    for i in range(start_page+1,end_page):
        if len(data[i])>1:

                if data[i][1][0]=="(" and data[i][1][1:data[i][1].index(")")].replace(" ","").isalpha() :
                    if data[i][2][0].isnumeric():
                        countx+=1
                        main.append(each)
                        each = []
                        each.extend(data[i])                    
                else:
                    each.extend(data[i])

    main.append(each)                   
    main.pop(0)

    first_details = []
    for i in range(len(main)):

        first_details.append([main[i][0],main[i][1],main[i][2]])  


    columns = ["Name","Party Affiliation","Constituency No.", "Constituency","Election year"]
    #columns.extend(["Unnamed"+str(i) for i in range(13)])

    first = []
    for i in first_details:
        first.append([i[0],i[1],i[2][0:2].replace("-",""),i[2][2:-5].strip("-"),year])


    maps = {"Summary":0} 
    a = main[0]
    column = []
    count =  1
    for i in a:
        if i.find("Voting")!=-1:
            break
        elif i.find(":")!=-1:
            column.append(i.split(":")[0])
            maps[i.split(":")[0].strip()] = count
            count+=1


    all_data = []
    for m in range(len(main)):
        a = main[m]
        candidate = ["" for i in range(40)]


        suit = ""
        summary = []
        sumc = 0

        for i in a:
            if i.find("Voting")!=-1:
                break
            else:
                if i.find(":")!=-1:
                    ind = i.index(":")
                    category = " ".join(i[:ind].lower().split())
                    if find_suitable(maps,category)!=-1:
                        suit = find_suitable(maps,category)
                        candidate[maps[suit]] = i[ind+1:]
                    else:
                        maps[category] = count
                        candidate[maps[category]] =i[ind+1:]
                        count+=1
                elif suit != "":
                    candidate[maps[suit]] += " "+ i
                elif suit=="" and sumc==3:
                    if find_suitable(maps,"Summary")!=-1:

                        candidate[maps["Summary"]] +=i
                    else:
                        maps["Summary"] = count
                        candidate[maps["Summary"]] +=i


            sumc+=1
        first[m].extend(candidate)
        all_data.append(first[m])

    others = list(maps.keys())
    columns.extend(others)


    for i in range(len(all_data)):
        all_data[i] = all_data[i][0:len(columns)]

    data = pd.DataFrame(all_data,columns = columns)
    data.to_csv(file[:-3]+"csv")
    print("Finished Scraping " + file +" results are in " + file[:-3]+"csv" )
