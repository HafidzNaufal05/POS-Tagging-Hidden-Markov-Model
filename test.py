import library.library as lib
import itertools as o 
import library.newlibrary as lib2

def uji_ayat(loop,ayat,tf):
    f = open("data/dataproses/data_uji.csv","r")
    fs = f.readlines()
    f.close()

    l_route = []
    route = lib.CreateRoute(ayat)
    dict_tag_count = lib.CountTag()
    choosen_route = route[0]
    score = 0
    counter = 0
    for x in route:
        i = 0
        if not loop:
            print("*****************Jalur " + str(counter+1) +"*****************")
            print(x)
            print()
        sum1 = 0
        while i < len(x) - 1:
            f_tag = x[i]
            s_tag = x[i+1]
            if not loop:  
                print("jumlah score "+ str(f_tag) + "-" + str(s_tag) + ": "+ str(dict_tag_count[(f_tag,s_tag)]))
            
            sum1 += int(dict_tag_count[(f_tag,s_tag)])
            i += 1
        if not loop:
            print("\ntotal score : " + str(sum1))
        

        if score < sum1:
           score = sum1
           choosen_route = x
        
        counter += 1


    f = open("data/dataproses/data_uji_pembanding.csv","r")
    fs2 = f.readlines()
    f.close()

    if not loop:
        
        x = fs2[ayat-1].split("(")
        route = []
        for tag in x:
            tag = tag.split("=")
            route.append(tag[1].rstrip("\n"))
            
        print("____________________________")
        str1 = " "
        print("Ayat : " + str1.join(fs[ayat-1].split("=")))
        print("Jalur sebenarnya : "+ str(route))
        print("Score : " + str(score))
        print("Jalur terpilih : " + str(choosen_route))
    else:
        tf = Compare2List(route[0],choosen_route,tf)
    return tf

def Compare2List(list1,list2,list3):
    i = 0
    while i < len(list1):
        if list1[i] == list2[i]:
            list3[0] += 1
        else:
            list3[1] += 1
        i += 1
    
    return list3

    
    
            

    

#lib.CreateDictionaryWord() #clear
#lib.CreateDictionaryAyat() #clear
#lib.PartitionData([10,2,3],5) #clear
#lib.CreateRoute() #clear
#lib.CountTag() #clear

def SetUniqueList(list1):
    unique1 = []
    for val in list1:
        if val not in unique1:
            unique1.append(val)
    return unique1



def testes():

    #lib.CreateDictionaryAyat()
    #lib.PartitionData([7,1,2],5)
    list_tag = list(lib.GetUniqueTag(1))
    d_tag,l_tag_ayats = lib.CountTagInTraining(list_tag)
    d_emisi = lib.Emisi(list_tag,d_tag)
    d_trans = lib.Transisi(list_tag,l_tag_ayats)
    f = open("data/dataproses/data_uji.csv","r")
    fs = f.readlines()
    f.close()
    lib.Metode(fs[0],d_trans,d_emisi,list_tag)
    #print(d)
    #emisi = lib.Emisi()
    
def AddSEInDictTag(tag_latih_trans,list_tag,list_2tag):
    d_2tag = lib2.my_dictionary()
    print("*******************\n\n\n***************")
    print(list_tag)
    for tag in list_tag:
        f_tag = "S" , tag
        e_tag = tag , "E"
        d_2tag.add(f_tag,0)
        d_2tag.add(e_tag,0)
    for tag in list_2tag:
        d_2tag.add(tag,0)
    print(tag_latih_trans)
    for tag_latih in tag_latih_trans: 
        key_f = "S",tag_latih[0]
        key_e = tag_latih[-1],"E"
        d_2tag.add(key_f, d_2tag[key_f] + 1)
        d_2tag.add(key_e, d_2tag[key_e] + 1)
    #print(d_2tag)
    return d_2tag

def remove(word,list1):
    for x in list1:
        word.replace(x,"")
    return word

def uji(tag_latih_trans,ayat):
    #f = open("data/dataproses/data_uji.csv","r")
    #fs = f.readlines()
    #f.close()

    #ayat = fs[1]
    #print(ayat)

    f = open("data/dataproses/Emition.csv","r")
    fs = f.readlines()
    f.close()

    list_tag = []  
    for dicty in fs:
        dicty = dicty.split("=")[0]
        tag = dicty.split(":")[1]
        list_tag.append(tag)
    list_tag_unique_training = SetUniqueList(list_tag) # tag unique from data training
    
    d_count_tag = CountTag(list_tag_unique_training)
    #create dictionary posibility emition from data training
    d_emition = lib2.csv_to_dict("data/dataproses/Emition")
    d_testing_emition = lib2.my_dictionary()
    #print(d_emition)
    ayat = ayat.split("=")
    for word in ayat:
        for tag in list_tag_unique_training:
            key = word.rstrip("\n"), tag
            if not d_emition.__contains__(key):
                #d_testing_emition.add(key,0.00000001)
                d_testing_emition.add(key,Laplace(d_count_tag,tag))
            else:
                d_testing_emition.add(key,d_emition[key])
    #print("s emisii test")
    #print(d_testing_emition)
    #print("e emisii test")

    #Pre dict transition
    list_tag_unique = lib2.GetUniqueTagTraining(1) #unique tag from ayat training
    list_2tag = lib2.GetUniqueTag(2)
    d_testing_transtion= AddSEInDictTag(tag_latih_trans,list_tag_unique,list_2tag) #kemungkinan 2tag yang ada pada data corpus
    d_transtion = lib2.csv_to_dict("data/dataproses/Transisi")
    #Metode
    
    #print(d_testing_transtion)
    keys = d_testing_transtion.keys()
    for key in keys:
        if d_transtion.__contains__(key):
            d_testing_transtion[key] = d_transtion[key]
        else:
            d_testing_transtion[key] = 0
    
    #print(d_testing_transtion)
    
    
    prev_tag = "S"
    prev_tag_temp = "S"
    prev_p = 1
    route = []
    for word in ayat:
        print("kata = {}".format(word))
        p = 0
        for tag in list_tag_unique:
            p_temp = d_testing_emition[(word.rstrip("\n"),tag)] * d_testing_transtion[(prev_tag,tag)] * prev_p
            #print(prev_tag,tag,prev_p)
            print("emisi * transisi = {} * {} * {} = {}".format(d_testing_emition[(word.rstrip("\n"),tag)],d_testing_transtion[prev_tag,tag],prev_p,p))
            if p <= p_temp:
                p = p_temp
                transisi = (prev_tag,tag)
                emistion = (word.rstrip("\n"),tag)
                prev_tag_temp = tag
        prev_tag = prev_tag_temp
        prev_p = p
        route.append(prev_tag)

        print("\n*****************")
        print("nilai p : {} transisi : {} emisi : {}".format(p,transisi,emistion))
        print("*****************\n")
    print("tag jalur = {}".format(route))
    return route


def CountTag(list_tag_unique):
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()

    dict1 = lib2.my_dictionary()
    for tag in list_tag_unique:
        dict1.add(tag,0)
    
    for ayat in fs:
        ayat = ayat.split("(")
        for word in ayat:
            tag = word.split("=")[1].rstrip("\n")
            
            if tag != "DET":
                dict1.add(tag,dict1[tag] + 1)
    
    #lib2.dict_to_csv(dict1,"data/dataproses/count_tag")
    return dict1
    
def Laplace(d_count_tag,tag):
    f = open("data/dataproses/data_latih.csv","r")
    fs = f.readlines()
    f.close()
    sum_word = 0

    
    for ayat in fs:
        ayat = ayat.split("(")
        sum_word += len(ayat)
        
            
    
    laplace = (0 + 1) / (d_count_tag[tag] + sum_word)
    return laplace
        
#clear
def testes2():
    list_tag = list(lib2.GetUniqueTag(1))
    lib2.CreateDictionaryWord()
    lib2.CreateDictionaryAyat()
    lib2.PartitionData([10,3,4],17)
    #print(list_tag)
    tag_latih_trans,d_trans = lib2.Transition()
    #print(d_trans)
    #print(tag_latih_trans)
    d_emition = lib2.Emition()
    #print(d_emition)

    lib2.dict_to_csv(d_trans,"data/dataproses/Transisi")
    lib2.dict_to_csv(d_emition,"data/dataproses/Emition")
    print("\n\n\n")
    print("Kasus al-fatihah dengan pertisi 7 dan panjang kata 20 serta data uji untuk ayat 1 dan 2\n")
    print("cek file transisi dan emisi ada pada dataproses")
    f = open("data/dataproses/data_uji.csv","r")
    fs = f.readlines()
    f.close()
    pilihan = 10
    i = 0
    routes = []
    for ayat in fs:
        if pilihan == 0:
            print("ayat yang diujikan\n{}".format(ayat.rstrip("\n")))
            route = uji(tag_latih_trans,ayat)
            routes.append(route)
            print("************\n\n")
        else:
            i += 1
            if pilihan == i:
                print("ayat yang diujikan\n{}".format(ayat.rstrip("\n")))
                route = uji(tag_latih_trans,ayat)
                routes.append(route)
                break
    print("\n\n")
    Compare(routes)
    #clear ^^

def Compare(routes):
    f = open("data/dataproses/data_uji_pembanding.csv","r")
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
    i = 0
    new_routes = []
    t = 0
    f = 0
    while i < len(routes):
        j = 0 
        while j < len(routes[i]):
            
            if list_tag_latih[i][j] != "DET":
                if routes[i][j] == list_tag_latih[i][j]:
                    t += 1
                else:
                    f += 1

            j += 1
        i += 1
    print("benar = {} | salah = {} | akurasi = {}%".format(t,f,round(t/(f+t) * 100)))


def a():
    print("s")
    k = list(o.product(["A","B","C","D"],repeat=5))
    for x in k:
        print(x)
a()