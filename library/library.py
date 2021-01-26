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

def GetUniqueTag(param):
    f = open("data/dataset/fullcorpus.txt","r")
    fs = f.readlines()
    f.close()

    l_tag = []
    for x in fs:
        x = x.split("\t")
        l_tag.append(x[2])

    l_tag = SetUniqueList(l_tag)
    return o.product(l_tag, repeat=param)



def CountTagInTraining(list_tag):
    
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()

    d_tag = my_dictionary()
    list_tag_ayats = []
    for words in fs:
        words = words.split("(")
        l_tag_ayat = []
        l_tag_ayat.append("S")
        for word in words:
            word_tag = word.split("=")[1].rstrip("\n")
            l_tag_ayat.append(word_tag)
            for tag in list_tag:
                if tag[0] == word_tag:
                    if d_tag.__contains__(tag[0]):
                        d_tag.add(tag[0],d_tag[tag[0]]+1)
                    else:
                        d_tag.add(tag[0],1) 
        l_tag_ayat.append("E")
        list_tag_ayats.append(l_tag_ayat)

    for tag in list_tag:
        if not d_tag.__contains__(tag[0]):
            d_tag.add(tag[0],0)
    
    return d_tag,list_tag_ayats
    

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

def Transisi(l_tag,l_tag_ayats):
    list_2_tag = list(GetUniqueTag(2))
    for tag in l_tag:
        list_2_tag.append(("S",tag[0]))
        list_2_tag.append((tag[0],"E"))
    
    #create dictionary 2 tag
    d_2tag = my_dictionary()
    for tag2 in list_2_tag:
        d_2tag.add(tag2,0)

    for l_tag_ayat in l_tag_ayats:
        i = 0
        while i < len(l_tag_ayat)-1:
            tag1 = l_tag_ayat[i]
            tag2 = l_tag_ayat[i+1]
            d_2tag[(tag1,tag2)] += 1
            i += 1
    
    return d_2tag


def Metode(ayat,d_trans,d_emisi,l_tag):
    

    
    fs = 0

    keys = list(d_emisi.keys())
    mat = []
    
    ayat = ayat.split("=")
    for word in ayat:
        row = []
        l_key = []
        word = word.rstrip("\n")
        same = 0
        print(word)
        for key in keys:
            if key[0] == word:
                same = 1
                l_key.append(key)
        if same == 0:
            for tag in l_tag:
                d_emisi.add((word,tag[0]),0.0)
                l_key.append((word,tag[0]))
            
        for key in l_key:
            row.append((key,d_emisi[key]))
        mat.append(row)
    
    print(d_trans)
    for row in mat:
        for val in row:
            print(val)

        



def Metodelame(ayat,d_2tag,d_emisi,l_tag):
    

    
    fs = 0

    keys = list(d_emisi.keys())
    mat = []
    for words in fs:
        words = words.split("=")
        for word in words:
            row = []
            l_key = []
            word = word.rstrip("\n")
            same = 0
            for key in keys:
                if key[0] == word:
                    same = 1
                    l_key.append(key)
            if same == 0:
                for tag in l_tag:
                    d_emisi.add((word,tag[0]),round(0,2))
                    l_key.append((word,tag[0]))
            
            for key in l_key:
                row.append((key,d_emisi[key]))
            

    
                    

def Transpose(m):
    mat = m
    row = len(mat)
    col = len(mat[0])
    newMat = []
    newMat = CreateZeroMatrix(col,row)
    i=0
    while i < row:
        y = 0
        while y < col:
            newMat[y][i] = mat[i][y]
            y +=1
        i += 1
    return newMat

def CreateZeroMatrix(n,m):
    mat = []
    for i in range(n):
        arrC = []
        for j in range(m):
            elm = Element(0,i,j)
            arrC.append(0)
        mat.append(arrC)
    return mat