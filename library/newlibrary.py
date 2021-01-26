import itertools as o 

#For make dictionary
class my_dictionary(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

class my_word(dict):
    def __init__(self,word,tp): 
        self.word = word
        self.tp = tp 
    def __str__(self):
        self.__s = "word : " + str(self.word) + " | type : " + str(self.tp)
        return self.__s

def SetUniqueList(list1):
    unique1 = []
    for val in list1:
        if val not in unique1:
            unique1.append(val)
    return unique1

def CreateDictionaryAyat():
    f = open("data/dataset/corpus.txt","r")
    fs = f.readlines()
    f.close()
    
    counter = 0
    ayat = ""
    #i = 0
    f = open("data/dataproses/kamus_ayat.csv","w+")
    for x in fs:
        x = x.split("\t")
        if counter != x[0].split(":")[1]:
            if counter != 0:
                f.write(ayat[:-1] + "\n")
            counter = x[0].split(":")[1]
            ayat = ""
        tag = x[2]
        word = x[1]
        ayat += word + "=" + tag + "("
    f.write(ayat[:-1] + "\n")
    f.close()

def CreateNewDataSetByLengthWord(word_length):
    
    f =open("data/dataproses/kamus_ayat.csv","r")
    fs = f.readlines()
    f.close()
    f1 = open("data/dataproses/kamus_ayat" + str(word_length) + ".csv","w+")
    
    for x in fs:
        l_word = x.split("(")
        new_l_word = l_word[0:word_length]
        i = 0
        for word in new_l_word:
            word = word.replace("\n","")
            f1.write(str(word))
            i+=1
            if(len(new_l_word) > word_length):
                if(i==word_length):
                    f1.write("\n")
                else:
                    f1.write("(")
            else:
                if(i==len(new_l_word)):
                    f1.write("\n")
                else:
                    f1.write("(")   
    f1.close()    

def PartitionData(param_partisi,param2):
    i = 0
    CreateNewDataSetByLengthWord(param2)
    f =open("data/dataproses/kamus_ayat"+ str(param2) +".csv","r")
    fs = f.readlines()
    f.close()
    l = len(fs)

    i = 0
    file_location = []
    for x in fs:
        
        if(i % int(l/(param_partisi[0]-1)) == 0):
            f1 = open("data/dataproses/data_partisi_"+ str(int(i/(int(l/(param_partisi[0]-1))))+1) +".csv","w+")
            file_location.append("data/dataproses/data_partisi_"+ str(int(i/(int(l/(param_partisi[0]-1))))+1) +".csv")
        l_word = x.split("(")
        f1.write(x)
        i+=1
    f1.close() 

    i = 0 
    fs = []
    while (i < len(param_partisi) - 1):
        f = open("data/dataproses/data_partisi_" + str(param_partisi[i+1]) + ".csv","r")
        t_fs = f.readlines()
        fs += t_fs
        i += 1
    f.close()
    i = 0
    while( i< len(param_partisi)-1):
        file_location.remove("data/dataproses/data_partisi_"+ str(param_partisi[i+1]) +".csv")
        i += 1
    i = 0
    latih_fs = []
    while(i < len(file_location)):
        f = open(file_location[i],"r")
        t_fs = f.readlines()
        latih_fs += t_fs
        i += 1
    f1 = open("data/dataproses/data_latih.csv","w+")
    f2 = open("data/dataproses/data_uji_pembanding.csv","w+")
    f3 = open("data/dataproses/data_uji.csv","w+")
    for x in fs:
        f2.write(x)
        x = x.replace("\n",",")
        x = x.split("(")
        j = 0
        for word in x:
            word = word.split("=")
            f3.write(word[0])
            if(j == len(x)-1):
                f3.write("\n")
            else:
                f3.write("=")
            j+=1
    for x in latih_fs:
        f1.write(x)
    f1.close()
    f2.close()
    f3.close()

def GetUniqueTagFull(param):
    f = open("data/dataset/fullcorpus.txt","r")
    fs = f.readlines()
    f.close()

    l_tag = []
    for x in fs:
        x = x.split("\t")
        l_tag.append(x[2])

    l_tag = SetUniqueList(l_tag)
    return o.product(l_tag, repeat=param)

def GetUniqueTag(param):
    f = open("data/dataset/corpus.txt","r")
    fs = f.readlines()
    f.close()

    l_tag = []
    for x in fs:
        x = x.split("\t")
        l_tag.append(x[2])

    l_tag = SetUniqueList(l_tag)
    l_tag = o.product(l_tag, repeat=param)
    list1 = []
    for x in l_tag:
        if param == 1:
            list1.append(x[0])
        else:
            list1.append(x)
    
    return list1

def GetUniqueTagTraining(param):
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()

    l_tag = []
    for ayat in fs:
        ayat = ayat.split("(")
        for word in ayat:
            tag = word.split("=")[1].rstrip("\n")
            
            l_tag.append(tag)


    l_tag = SetUniqueList(l_tag)
    l_tag = o.product(l_tag, repeat=param)
    list1 = []
    for x in l_tag:
        if param == 1:
            list1.append(x[0])
        else:
            list1.append(x)
    
    return list1

def CreateUniqueWord():
    f = open("data/dataset/corpus.txt","r")
    fs = f.readlines()
    f.close()

    
    list_word = []
    for words in fs:
        words = words.split("\t")
        list_word.append(words[1])

    list_word = SetUniqueList(list_word)
    #print(list_word)
    f = open("data/dataproses/UNIQUE_WORD2.csv","w+")
    for word in list_word:
        f.write(str(word)+"\n")
    f.close()

def CreateDictionaryWord():
    CreateUniqueWord()
    f = open("data/dataproses/UNIQUE_WORD2.csv","r")
    fs = f.readlines()
    f.close()

    

    f = open("data/dataset/corpus.txt","r")
    fs2 = f.readlines()
    f.close()

    f = open("data/dataproses/kamus_kata.csv","w+")
    for word in fs:
        
        word = word.rstrip("\n")
        l_tag = []

        for row in fs2:
            tag = row.split("\t")
            if word == tag[1]:
                l_tag.append(tag[2])
        
        l_tag = SetUniqueList(l_tag)
        tags = ""
        for tag in l_tag:
            tags += tag+"("

        f.write(word + "=" + tags[:-1] + "\n")
    
    f.close()

def Emisi(l_tag,d_tag):
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()

    
    d_emisi = my_dictionary()
    l_word = []
    for words in fs:
        words = words.split("(")
        for word in words:
            word_tag = word.split("=")[1].rstrip("\n")
            word = word.split("=")[0]
            if d_emisi.__contains__((word,word_tag)):
                d_emisi.add((word,word_tag),d_emisi[(word,word_tag)] + 1)
            else:
                d_emisi.add((word,word_tag),1)
            l_word.append(word)

    l_word = SetUniqueList(l_word)
    #print(len(list(d_emisi)))
    for tag in l_tag:
        for word in l_word:
            if not d_emisi.__contains__((word,tag[0])):
                d_emisi.add((word,tag[0]),0)
    #print(len(list(d_emisi.keys())))

#    d_tag = CountTagInTraining()
    for key in d_emisi.keys():
        if d_tag[key[1]] != 0:
            d_emisi[key] = round(d_emisi[key] / d_tag[key[1]],2)
        else:
            d_emisi[key] = 0.0
    
    return d_emisi


def CountTag(list_tag_unique):
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()

    dict1 = my_dictionary()
    for tag in list_tag_unique:
        dict1.add(tag,0)
    
    for ayat in fs:
        ayat = ayat.split("(")
        for word in ayat:
            tag = word.split("=")[1].rstrip("\n")
            
            
            dict1.add(tag,dict1[tag] + 1)
    dict1.add("S",len(fs))
    dict1.add("E",len(fs))
    #lib2.dict_to_csv(dict1,"data/dataproses/count_tag")
    return dict1


def CountTagTransition(list_tag_unique):
    f = open("data/dataproses/Transisi.csv","r")
    fs = f.readlines()
    f.close()

    dict1 = my_dictionary()
    for tag in list_tag_unique:
        dict1.add(tag,0)
    
    for f_tag in fs:
        count = int(f_tag.split(":")[1].split("=")[1].rstrip("\n"))
        f_tag = f_tag.split(":")[0]    
        dict1[f_tag] += count
        
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()
    dict1.add("S",len(fs))
    dict1.add("E",len(fs))
   # print(dict1)
    return dict1

def Transition():
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()
    
    list_tag_latih = []
    for ayat in fs:
        ayat = ayat.split("(")
        ayat_tag = []
        for word in ayat:
            
            tag = word.split("=")[1]
            
            
            ayat_tag.append(tag.rstrip("\n"))
        list_tag_latih.append(ayat_tag)
    
    d_trans = my_dictionary()        
    for tags in list_tag_latih:
        
        #tags = ["S"] + tags + ["E"]
        #print(tags)
        i = 0
        while i < len(tags) - 1:
            key = (tags[i],tags[i+1])
            #print(key)
            if d_trans.__contains__(key):
                d_trans.add(key,d_trans[key] + 1)
            else:
                d_trans.add(key,1)
            i += 1
    

    return list_tag_latih, d_trans


def Emition():
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()

    d_emition = my_dictionary()

    for ayat in fs:
        ayat = ayat.split("(")
        ayat_tag = []
        for word in ayat:
            tag = word.split("=")[1]
            word = word.split("=")[0]
            
            key = (word,tag.rstrip("\n"))
            if d_emition.__contains__(key):
                d_emition.add(key,d_emition[key] + 1)
            else:
                d_emition.add(key,1)

    return d_emition

def dict_to_csv(dict1,nm_file):
    f = open(str(nm_file)+".csv","w+")
    
    

    val = False
    #print()
    #row = len(dict1[list(dict1.keys())[0]])
    row = len(list(dict1.keys()))
    k=0
    i=0
    for key in dict1.keys():
        f.write(str(key[0]) + ":" + str(key[1]) + "=" + str(dict1[key]) + "\n")
         
    f.close()

def csv_to_dict(nm_file):
    f = open(str(nm_file)+".csv","r")
    fs = f.readlines()
    f.close()
    
    dicty1 = my_dictionary()
    for row in fs:
        val = float(row.split("=")[1].rstrip("\n"))
        tag1 = row.split("=")[0].split(":")[0]
        tag2 = row.split("=")[0].split(":")[1]
        dicty1.add((tag1,tag2),val)
    return dicty1

