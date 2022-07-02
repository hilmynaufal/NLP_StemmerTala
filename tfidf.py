import csv
import numpy as np
import pandas as pd
import math
import re
    
def delPrefix(str,prx):
    if str.startswith(prx):
        rootWord= str.removeprefix(prx)
        # print(rootWord)
        return rootWord
    else:
        # print("gagal remove prefix")
        return str
       
def delSuffix(str,sfx):
    if str.endswith(sfx):
        rootWord= str.removesuffix(sfx)
        return rootWord
    else:
        # print('gagal remove suffix')
        return str
   
def main():
    awalan2 =  np.loadtxt('awalan2.txt',dtype="U")
    akhiran = np.loadtxt('akhiran.txt',dtype="U")
    stopWords = np.loadtxt('stopword.txt',dtype="U")
    cStop=len(stopWords)
    # print("Jumlah dokumen: ")
    # jml = input()
    # documents = list()
    # for x in range(int(jml)):
    #     print("dokumen ke-" + str(x+1) + ": ")
    #     documents.append(input())
    text_file = open("novel.txt", "r")
    novel =' '.join(text_file.readlines())
    documents=[novel]

    
    #membuat token
    tersplit = []
    d = list()
    d_index = list(list())
    for document in documents:
        tersplit.append(" ".join(re.findall("[a-zA-Z]+", document)).split(" "))

    #to lowercase
    temp_lower = list()
    for x in tersplit:
        temp_lower1 = list()
        for y in x:
            temp_lower1.append(y.lower())
        temp_lower.append(temp_lower1)
    tersplit.clear()
    tersplit = temp_lower
    
    for x in tersplit:
        for y in x:
            if y not in d and y not in stopWords:
                d.append(y)

   
    for x in tersplit:
        d_index_temp = []
        for y in d:
            d_index_temp.append(x.count(y))
        d_index.append(d_index_temp)

    # tahap 4 algoritma Tala 
    for i in range(len(akhiran)):
       tesString = "persaudaraan"
       rootword=delSuffix(tesString, akhiran[i])
       if tesString is not rootword:
         for j in range(len(awalan2)):
            rootword=delPrefix(rootword, awalan2[j])
         break
    print(rootword)
    # tahap 5 algoritma Tala     
    tesString = "bersamaan"       
    for i in range(len(awalan2)):
       rootword=delPrefix(tesString, awalan2[i])
       if tesString is not rootword:
        # print(rootword)
        break
    tesString = rootword
    for i in range(len(akhiran)):
       rootword=delSuffix(rootword, akhiran[i])
       if tesString is not rootword:
        print(rootword)
        break
    
    #buat column
    dic = dict()
    dic.update({'Token':d})
    header = list()
    header.append("Token")
    for idx, val in enumerate(d_index):
        # s = 'D' + str(idx+1)
        s = 'Frekuensi kata' 
        header.append(s)
    for idx, val in enumerate(d_index):
        dic.update({header[idx+1]:d_index[idx]})

    
    
    # #hitung tf
    # tf = list()
    # n = list()
    # for idx, val in enumerate(d_index):
    #     temp = list()
    #     s = 'Tf' + str(idx+1)
    #     header.append(s)
    #     for y in val:
    #         if y <= 0:
    #             temp.append(y)
    #         else:
    #             temp.append(round(1+math.log(y, 10), 3))
    #     tf.append(temp)
    #     dic.update({s:tf[idx]})


    # #hitung n
    # header.append('n')
    # for idx, val in enumerate(d_index):
    #     for x, val1 in enumerate(val):
    #         if len(n) < len(val):
    #             n.append(0)
    #         if val1 != 0:
    #             n[x] += 1
    # dic.update({'n':n})

    # #hitung idf
    # idf = list()
    # header.append('idf')
    # for x in n:
    #     idf.append(math.log10(4/x))
    # dic.update({'idf':idf})

    # #hitung tf-idf
    # tf_idf = list()
    # for idx, val in enumerate(tf):
    #     s = 'Tf-idf' + str(idx+1)
    #     header.append(s)
    #     temp = list()
    #     for x, val1 in enumerate(val):
    #         temp.append(val1*idf[x])
    #     tf_idf.append(temp)
    #     dic.update({s:temp})

    #export
    data = pd.DataFrame.from_dict(dic)
    data = data.round(decimals=3)
    data.to_excel('test.xlsx', sheet_name="sheet1", index=False)
    print("ekstrak token berhasil, silahkan buka file test.xlsx")
    

main()