#code for metadata of 1st and 2nd election judgement documents and 2nd document scraping

import pandas as pd
import pdftotext
import os


#all_files = os.listdir()

#all_files = [ i for i in all_files if i[-3:]=="pdf" ]
#all_files.sort()



def create_ds(a):

    with open(a, "rb") as f:
            pdf = pdftotext.PDF(f)

    data = []
    for i in range(len(pdf)):
        data.append(pdf[i])

    index = data[2:5]

    for i in range(len(index)):
        index[i] = index[i].split("\n")

    all_cases_index = []
    for i in range(len(index)):
        all_cases_index.extend(index[i])

    b = all_cases_index

    while "" in b:
        b.remove("")

    li = []
    l= []
    count = 1
    for i in b:
        if i[0:2].find(str(count))!=-1:
            li.append(l)
            l  = []
            l.append(i[:-4])
            count+=1
        else:
            l.append(i)

    li.append(l)





    li.pop(0)

    for i in range(len(li)):
        li[i] = [k.strip() for k in li[i]]
        li[i] = " ".join(li[i])

    subjects = []
    courts = []
    for i in li:
        if i.find("Vs")!=-1:

            start = i.find("Vs")

        if i.find("(")!=-1:
            ind = i.find("(")
            subject = i[:ind][3:].strip()
            court = (i[ind:])
            subjects.append(subject)
            courts.append(court)



    for i in range(len(data)):
        data[i] = data[i].split("\n")

    for i in range(len(courts)):
        inds = courts[i].find("(")
        inde = courts[i].find(")")
        courts[i] = courts[i][inds+1:inde]

    courts[16] = "Supreme Court of India"

    courts[-9] = "Supreme Court of India" 

    subjects[16]

    all_cases = []

    for i in data:
        all_cases.extend(i)

    curr = courts[0].upper()

    count = 0

    for i in all_cases:
        if i.find(curr)!=-1:

            count+=1
            curr = courts[count].upper()



    len(courts)

    len(subjects)

    metadata = pd.DataFrame()

    metadata["court"] =courts

    metadata["subject"] = subjects



    vol1 = metadata[0:10]
    vol2 = metadata[10:]

    #f = all_files[1]
	
    f = a

    with open(f, "rb") as f:
            pdf = pdftotext.PDF(f)

    data = []
    for i in range(len(pdf)):
        data.append(pdf[i])

    ## data

    data = data[4:]

    for i in range(len(data)):
        data[i] = data[i].split("\n")

    all_text = []

    for i in data:
        all_text.extend(i)

    co = list(vol2["court"])

    for i in range(len(co)):
        co[i]= co[i].upper()

    count = 0

    for i in all_text:
        if i.find(co[count])!=-1:
            print(i)
            count+=1



    co.append("HIGH COURT OF ANDHRA PRADESH")

    co.append("HIGH COURT OF JUDICATURE AT ALLAHABAD")

    co.append("HIGH COURT OF PUNJAB & HARYANA")

    def if_any(i):
        result = False
        for j in set(co):
            if i.find(j)!=-1 and len(i.split())==len(j.split()):
                result = True
                break
        return result

    all_cases = []
    case = []

    for i in all_text:
        if if_any(i):
            all_cases.append(case)
            case = []
            case.append(i)
        else:
            case.append(i)
    all_cases.append(case)


    len(all_cases)

    all_cases.pop(0)



    all_details = []

    for i in all_cases:
        cour = i[0].strip()
        appeal = i[1]
        for j in i:
            if j.lower().find("appellant")!=-1 or j.lower().find("petitioner")!=-1 :
                app = j.split("..")[0].strip()
                break
        for j in i:
            if j.lower().find("respondent")!=-1 :
                res = j.split("..")[0].strip()

                break


        for j in range(len(i)):
            if i[j].find("SUMMARY OF THE CASE")!=-1:
                summ = i[j].strip()
                break
        st = j+1
        #print(app)
        #print(res)

        for j in range(len(i)):
            if i[j].find("JUDGMENT")!=-1:
                break
        end = j
        summary = " ".join(i[st:end])
        subj = app + " vs " + res
        print(subj)
        #print(summary)

        appeal = ""
        for j in range(len(i)):
            if i[j].find("No")!=-1:
                appeal = i[j].strip()
                break

        for j in range(len(i)):
            if i[j].find("dated")!=-1:
                dec = i[j].strip()[i[j].strip().find("dated")+5:-1]
                break





        judg = "NIL"
        for j in range(len(i)):
            if i[j].find("JUDGMENT")!=-1:
                judg = i[j+1:]
                break

        all_details.append([cour,appeal,dec,subj,app,res,summary,judg])






    all_details = pd.DataFrame(all_details,columns = ["court","appeal no.","date","subject","appellant","respondent","summary","judgment"])

    all_details.to_csv(a+".csv")


if __name__ == "__main__":
    import sys
    import pdftotext
    import pandas as pd
    import os
    create_ds(sys.argv[1])
    
