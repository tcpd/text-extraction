
def find_metric(file):
    total = 0
    total_sp = 0
    total_c = 0
    
    with open(file, 'rb') as f:
        pdf = pdftotext.PDF(f)


    data = []
    for i in range(len(pdf)):
        data.append(pdf[i])

    for i in range(len(data)):
        data[i] = " ".join(data[i].split("\n")).strip()

    data = data[5:]

    for i in data:
        if len(i)==0:
            continue

        i = i.replace(" ","")
        count = 0
        for j in i:
            if not j.isalnum():
                count+=1
                
        total_sp+=count
        total_c+= len(i)
        #print("total = ",len(i))
        #print("special = ", count)
        ratio = count/len(i)
        #print("ratio = ",ratio)
        
    return total_sp/total_c

if __name__ == "__main__":
	import sys
	import pdftotext
	import pandas as pd
	import os
	b = find_metric(sys.argv[1])
	print(b)

