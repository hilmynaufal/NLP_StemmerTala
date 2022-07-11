import csv
import numpy as np
import pandas as pd
import math
import re
    
def delPrefix(str,prx):
    prx=prx.split(",")
    if len(prx) == 1 :
        if str.startswith(prx[0]):
            rootWord= str.removeprefix(prx[0])
            # print(rootWord)
            return rootWord
        else:
            # print("gagal remove prefix")
            return str
    else:
        if str.startswith(prx[0]):
            rootWord=prx[1]+str.removeprefix(prx[0])
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
    awalan1 =  np.loadtxt('awalan1.txt',dtype="U")
    awalan2 =  np.loadtxt('awalan2.txt',dtype="U")
    akhiran = np.loadtxt('akhiran.txt',dtype="U")
    kepunyaan = np.loadtxt('kepunyaan.txt',dtype="U")
    partikel = np.loadtxt('partikel.txt',dtype="U")
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

    stem = list()
    t_partikel = list()
    t_kepunyaan = list()
    t_awalan1 = list()
    t_awalan2 = list()
    t_akhiran = list()
    akhiran_temp = ""
    for j in d:
    # tahap 1 algoritma Tala
        tesString = j
        for i in range(len(partikel)):
            rootword=delSuffix(tesString, partikel[i])
            if tesString is not rootword:
                break
        tesString=rootword
        t_partikel.append(tesString)
        # tahap 2 algoritma Tala     
        for i in range(len(kepunyaan)):
            rootword=delSuffix(tesString, kepunyaan[i])
            if tesString is not rootword:
                break
        tesString=rootword
        t_kepunyaan.append(tesString)
        # tahap 3 algoritma Tala      
        for c in range(len(awalan1)):
            rootword=delPrefix(tesString, awalan1[c])
            if tesString is not rootword:
                break
        if tesString is not rootword:
            t_awalan1.append(rootword)
            tesString=rootword
            
            # tahap 4 algoritma Tala 
            for i in range(len(akhiran)):  
                rootword=delSuffix(tesString, akhiran[i])
                if tesString is not rootword:
                    t_akhiran.append(rootword)
                    for j in range(len(awalan2)):
                        rootword=delPrefix(rootword, awalan2[j])
                    break
                else:
                    akhiran_temp = rootword
                    
            if tesString is rootword:
                t_akhiran.append(akhiran_temp)
            tesString=rootword
            t_awalan2.append(tesString)
        else:
            t_awalan1.append(rootword)
            tesString=rootword
            # tahap 5 algoritma Tala        
            for i in range(len(awalan2)):
                rootword=delPrefix(tesString, awalan2[i])
                if tesString is not rootword:
                    # print(rootword)
                    break
            tesString = rootword
            t_awalan2.append(tesString)
            for i in range(len(akhiran)):
                rootword=delSuffix(rootword, akhiran[i])
                if tesString is not rootword:
                    break
            tesString=rootword
            t_akhiran.append(tesString)
        stem.append(tesString)
    
   
    #buat column
    dic = dict()
    dic.update({'Token':d})
    header = list()
    header.append("Token")
    for idx, val in enumerate(d_index):
        # s = 'D' + str(idx+1)
        s = 'Frekuensi kata' 
        z = 'Hasil Stemming'
        header.append(s)
        header.append("Tanpa partikel")
        header.append("Tanpa kepunyaan")
        header.append("Tanpa awalan1")
        header.append("Tanpa awalan2")
        header.append("Tanpa akhiran")
        header.append(z)
        
    for idx, val in enumerate(d_index):
        dic.update({header[idx+1]:d_index[idx]})
    dic.update({"Tanpa partikel":t_partikel})
    dic.update({"Tanpa kepunyaan":t_kepunyaan})
    dic.update({"Tanpa awalan1":t_awalan1})
    dic.update({"Tanpa awalan2":t_awalan2})
    dic.update({"Tanpa akhiran":t_akhiran})
    dic.update({'Hasil Stemming':stem})
    
  
    


    #export
    data = pd.DataFrame.from_dict(dic)
    
    data.to_excel('StemmingTala.xlsx', sheet_name="sheet1", index=False)
    print("ekstrak token berhasil, silahkan buka file StemmingTala.xlsx")
    

main()