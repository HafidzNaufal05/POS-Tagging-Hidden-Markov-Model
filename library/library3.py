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

def NewCreateDictionaryWord():
    f = open("data/dataset/UNIQUE_WORD2.csv","r")
    fs = f.readlines()
    f.close()

    f = open("data/dataset/corpus.txt","r")
    fs2 = f.readlines()
    f.close()

    f = open("data/dataset/new_kamus_kata.csv","w+")
    for word in fs:
        word = word.split(",")
        word = word[1]
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

def CreateDictionaryWord():
    f = open("data/dataset/UNIQUE_WORD2.csv","r")
    fs = f.readlines()
    f.close()

    f = open("data/dataset/properties2.txt","r")
    fs2 = f.readlines()
    f.close()

    f = open("data/dataset/kamus_kata.csv","w+")
    for word in fs:
        word = word.split(",")
        word = word[1]
        l_tag = []

        for row in fs2:
            tag = row.replace(" ","")
            tag = tag.split("|")
            if word == tag[5]:
                l_tag.append(tag[1])
        
        l_tag = SetUniqueList(l_tag)
        tags = ""
        for tag in l_tag:
            tags += tag+"("

        f.write(word + "=" + tags[:-1] + "\n")
    
    f.close()

def AddDictionaryPrefix():
    f = open("data/dataset/UNIQUE_PREFIX.csv","r")
    fs = f.readlines()
    f.close()

    f = open("data/dataset/corpus.txt","r")
    fs2 = f.readlines()
    f.close()

    f = open("data/dataset/NewPrefix.csv","w+")
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

def NewCreateDictionaryAyat():
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

def CreateDictionaryAyat():
    f = open("data/dataset/properties2.txt","r")
    fs = f.readlines()
    f.close()
    
    counter = 0
    ayat = ""
    #i = 0
    f = open("data/dataproses/kamus_ayat.csv","w+")
    for x in fs:
        x = x.replace(" ","")
        x = x.split("|")
        
        if counter != x[0].split(":")[1]:
            if counter != 0:
                f.write(ayat[:-1] + "\n")
            counter = x[0].split(":")[1]
            ayat = ""
        tag = x[1]
        word = x[5]
        ayat += word + "=" + tag + "("
    f.close()

def GetUniqueTag():
    f = open("data/dataset/fullcorpus.txt","r")
    fs = f.readlines()
    f.close()

    l_tag = []
    for x in fs:
        x = x.split("\t")
        l_tag.append(x[2])

    l_tag = SetUniqueList(l_tag)
    return o.product(l_tag, repeat=2)
    

    
        

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


#[2,3],10

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

def CreateRoute(param):
    f = open("data/dataproses/data_uji.csv","r")
    fs = f.readlines()
    f.close()

    f = open("data/dataset/kamus_kata.csv","r")
    fs2 = f.readlines()
    f.close()
    l_ayat = []
    i = 0
    if param != 0:
        param -= 1
        words = fs[param].split("=")
        #ayat = my_dictionary()
        ayat = []
        
        for word in words:
            word = word.rstrip("\n")
            for word_tag in fs2:
                tag_word = word_tag.split("=")[0]
                tags = word_tag.split("=")[1].split("(") #list tag
                l_tag = []
                for tag in tags:
                    l_tag.append(tag.rstrip("\n"))
                if word == tag_word:
                    ayat.append((word,l_tag))
                    break
    l_tag = []
    j = 0
    l_path = []
    for x in ayat:
        if x[1] == ['DET']:
            continue
        l_tag.append(x[1])
    
    for path in o.product(*l_tag):
        j += 1
        l_path.append(list(path))
    return l_path
    
        
def CreateRoute3(param):
    f = open("data/dataproses/data_uji.csv","r")
    fs = f.readlines()
    f.close()

    f = open("data/dataset/kamus_kata.csv","r")
    fs2 = f.readlines()
    f.close()
    l_ayat = []
    i = 0
    if param != 0:
        param -= 1
        words = fs[param].split("=")
        #ayat = my_dictionary()
        ayat = []
        
        for word in words:
            word = word.rstrip("\n")
            for word_tag in fs2:
                tag_word = word_tag.split("=")[0]
                tags = word_tag.split("=")[1].split("(") #list tag
                l_tag = []
                for tag in tags:
                    l_tag.append(tag.rstrip("\n"))
                if word == tag_word:
                    ayat.append((word,l_tag))
                    break
        
    n_route = 1
    for x in ayat:
        keys = x[1]        
        n_route *= len(keys)
        
    l_all_route = []
    
    l_route = []
    
    print(ayat)
    for x in ayat:
        i = 0
        l_ayat_route = []
        l_temp = x[1]

        while len(l_temp) < n_route:            
            l_temp = l_temp + x[1]            
        l_route.append(l_temp)
    i = 0
    l_route2= []
    while i < len(l_route[0]):
        j = 0
        temp = []
        while j < len(l_route):
            temp.append(l_route[j][i])
            j+=1
        l_route2.append(temp)
        i+=1

    

    return l_route2
                
        
def CreateRoute2(param):
    f = open("data/dataproses/data_uji.csv","r")
    fs = f.readlines()
    f.close()

    f = open("data/dataset/kamus_kata.csv","r")
    fs2 = f.readlines()
    f.close()
    l_ayat = []
    i = 0
    print(fs[param-1])
    if param != 0:
        param -= 1
        words = fs[param].split("=")
        ayat = my_dictionary()
        
        for word in words:
            word = word.rstrip("\n")
            for word_tag in fs2:
                tag_word = word_tag.split("=")[0]
                tags = word_tag.split("=")[1].split("(") #list tag
                l_tag = []
                for tag in tags:
                    l_tag.append(tag.rstrip("\n"))
                if word == tag_word:
                    ayat.add(word,l_tag)
                    break
        l_ayat.append(ayat)
        print(l_ayat)
    else:
        for row in fs:
            words = row.split("=")
            ayat = my_dictionary()
            for word in words:
                word = word.rstrip("\n")
                for word_tag in fs2:
                    tag_word = word_tag.split("=")[0]
                    tags = word_tag.split("=")[1].split("(") #list tag
                    l_tag = []
                    for tag in tags:
                        l_tag.append(tag.rstrip("\n"))
                    if word == tag_word:
                        ayat.add(word,l_tag)
                        break
            l_ayat.append(ayat)
            if i == 10:
                break
            i += 1
    j  =1
    
    #print(l_ayat)
    l_all_route = []
    for x in l_ayat:
        
        keys = x.keys()
        n_route = 1
        for key in keys:
            #print(x[key])
            pjg = len(x[key])
            n_route *= pjg
        i = 0
        #print(n_route)
        l_ayat_route = []
        
        l_route = []
        for key in keys:
            l_tag = x[key]
            #print(x)
            
            while len(l_tag) < n_route:
                l_tag += l_tag
            l_route.append(l_tag)
        l_ayat_route.append(l_route)
            

        #print(j)
        #print("*************************")
        #for r in l_ayat_route:
            #print(r)
        #j += 1
        
        l_route = []
        for i in range(0,len(l_ayat_route)):
            for k in range(0,n_route):
                temp = []
                for j in range(0,len(l_ayat_route[0])):                
                    temp.append(l_ayat_route[i][j][k])
                l_route.append(temp)
        return l_route            

        
            
def CountTag():
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()

    uniq_2tag = GetUniqueTag()
    dict_tag = my_dictionary()
    
    for tag in uniq_2tag:
        
        dict_tag.add(tag,0)

    
    for row in fs:
        row = row.split("(")
        i = 0
        l_2tag = []
        while i < len(row) - 1:
            f_tag = row[i].split("=")[1]
            if f_tag == 'DET':
                i += 1
                f_tag = row[i].split("=")[1]
            s_tag = row[i+1].split("=")[1].rstrip("\n")
            if s_tag == 'DET':
                i += 1
                s_tag = row[i+1].split("=")[1].rstrip("\n")
            
            i += 1
            l_2tag.append((f_tag,s_tag))
        
        
        for tag in l_2tag:
            dict_tag[tag] += 1

    f = open("data/dataproses/count_tag.csv","w+")
    #print("d")
    uniq_2tag = GetUniqueTag()
    for tag in uniq_2tag:
        
        f.write(str(tag) + ":" + str(dict_tag[tag]) + "\n")
    f.close()

    return dict_tag




                


    

