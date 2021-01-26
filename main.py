import library.newlibrary as lib
import time

visible = open("setting.txt","r").readline().split("=")[1]

def PrintTime(t):
    t = int(t)
    s = ""
    if(t/60>0):
        s += str(int(t/60)) +" menit " +str(t%60) +" detik"
    else:
        s += str(t%60) +" detik"
    print(s)

def AddSEInDictTag(tag_latih_trans,list_tag,list_2tag):
    d_2tag = lib.my_dictionary()
    
    for tag in list_tag:
        f_tag = "S" , tag
        e_tag = tag , "E"
        d_2tag.add(f_tag,0)
        d_2tag.add(e_tag,0)
    for tag in list_2tag:
        d_2tag.add(tag,0)
    
    for tag_latih in tag_latih_trans: 
        key_f = "S",tag_latih[0]
        key_e = tag_latih[-1],"E"
        d_2tag.add(key_f, d_2tag[key_f] + 1)
        d_2tag.add(key_e, d_2tag[key_e] + 1)
    #print(d_2tag)
    
    return d_2tag

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

def uji(loop,tag_latih_trans,ayat):

    f = open("data/dataproses/Emition.csv","r")
    fs = f.readlines()
    f.close()

    list_tag = []  
    for dicty in fs:
        dicty = dicty.split("=")[0]
        tag = dicty.split(":")[1]
        list_tag.append(tag)
    list_tag_unique_training = lib.SetUniqueList(list_tag) # tag unique from data training
    
    d_count_tag = lib.CountTag(list_tag_unique_training)
    #create dictionary posibility emition from data training
    d_emition = lib.csv_to_dict("data/dataproses/Emition")
    keys = d_emition.keys()
    for key in keys:
        d_emition[key] = d_emition[key] / d_count_tag[key[1]]
    d_testing_emition = lib.my_dictionary()
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
    d_count_tag = lib.CountTagTransition(list_tag_unique_training)
    #Pre dict transition
    list_tag_unique = lib.GetUniqueTagTraining(1) #unique tag from ayat training
    list_2tag = lib.GetUniqueTag(2)
    d_testing_transtion= AddSEInDictTag(tag_latih_trans,list_tag_unique,list_2tag) #kemungkinan 2tag yang ada pada data corpus
    d_transtion = lib.csv_to_dict("data/dataproses/Transisi")
    #Metode
    #print(d_testing_transtion)
    #print(d_testing_transtion)
    keys = d_testing_transtion.keys()
    #print(d_testing_transtion)
    #print(d_count_tag["S"])
    for key in keys:
        #print(key)
        if d_testing_transtion[key] == 0:
            if d_transtion.__contains__(key):
                
                d_testing_transtion[key] = d_transtion[key] / d_count_tag[key[0]]

                #print("transisi_u  = transi_l  / jml_tag = {} / {} = {}  ".format(d_transtion[key],d_count_tag[key[0]],d_testing_transtion[key]))
        else:
            if key[1] == "E":
                d_testing_transtion[key] = d_testing_transtion[key] / d_count_tag[key[1]]
            elif d_count_tag[key[0]] == 0:
                d_testing_transtion[key] = 0
            else:
                # if key[1] == "E":
                    
                #     d_testing_transtion[key] = d_testing_transtion[key] / d_count_tag[key[1]]
                # else:
                d_testing_transtion[key] = d_testing_transtion[key] / d_count_tag[key[0]]
                
            
    #print(keys)
    #for key in keys:
    #    if d_testing_transtion.__contains__(key):
            
    #        d_testing_transtion[key] = d_transtion[key]
    #    else:
    #        d_testing_transtion[key] = 0.000000000001
    
    #print(d_testing_transtion)
    
    
    #prev_tag = "S"
    #prev_tag_temp = "S"
    prev_v = 1
    route = []
    d_v_prev = lib.my_dictionary()
    d_v = lib.my_dictionary()
    d_v.add("S",[1])
    d_v_prev.add("S",[1])
    i = 0

    
    l = []

    tag_prev = "S"
    tag_prev_v = 0
    if not loop:
        file_result = open("result_test.txt","w+")
    for tag in list_tag_unique:
        d_v_prev.add(tag,[0])
    #lame
    for word in ayat:
        i += 1
        if not loop:
            print("kata = {}".format(word.rstrip("\n")))
        v = 0
        if i == 1:
            list1 = ["S"]
        else:
            list1 = list_tag_unique
        for tag in list_tag_unique:
            d_v.add(tag,[0])
            
        for prev_tag in list1:
            for tag in list_tag_unique:
               # print(d_testing_emition[(word.rstrip("\n"),tag)])
               # print(d_testing_emition[(word.rstrip("\n"),tag)])
               # print(d_v_prev[prev_tag])
                v_temp = d_testing_emition[(word.rstrip("\n"),tag)] * d_testing_transtion[(prev_tag,tag)] * max(d_v_prev[prev_tag])
                d_v[tag].append(v_temp)                    
                
                
                #### untuk lihat perhitungan ##########
                if not loop:
                    if i == len(ayat):
                        file_result.write("tag : {} , {} and tag : {} , E\n ".format(prev_tag,tag,tag))
                    else:
                        file_result.write("tag : {} , {}\n ".format(prev_tag,tag))
                if visible == "yes" and not loop:
                    print(prev_tag,tag)
                if i == len(ayat):
                    v_temp = d_testing_emition[(word.rstrip("\n"),tag)] * d_testing_transtion[(prev_tag,tag)] * d_testing_transtion[tag,"E"] * max(d_v_prev[prev_tag])
                    if not loop:
                        file_result.write("emisi * transisi * v_prev * transisi_end = {} * {} * {} * {}= {} \n".format(d_testing_emition[(word.rstrip("\n"),tag)],d_testing_transtion[prev_tag,tag],d_testing_transtion[tag,"E"],max(d_v_prev[prev_tag]),v_temp))
                    if visible == "yes" and not loop:
                        print("emisi * transisi * v_prev * transisi_end = {} * {} * {} * {}= {}".format(d_testing_emition[(word.rstrip("\n"),tag)],d_testing_transtion[prev_tag,tag],d_testing_transtion[tag,"E"],max(d_v_prev[prev_tag]),v_temp))
                else:
                    v_temp = d_testing_emition[(word.rstrip("\n"),tag)] * d_testing_transtion[(prev_tag,tag)] * max(d_v_prev[prev_tag])
                    if not loop:
                        file_result.write("emisi * transisi * v_prev = {} * {} * {} = {} \n".format(d_testing_emition[(word.rstrip("\n"),tag)],d_testing_transtion[prev_tag,tag],max(d_v_prev[prev_tag]),v_temp))
                    if visible == "yes" and not loop:
                        print("emisi * transisi * v_prev = {} * {} * {} = {}".format(d_testing_emition[(word.rstrip("\n"),tag)],d_testing_transtion[prev_tag,tag],max(d_v_prev[prev_tag]),v_temp))
                        
                #### akhir lihat perhitungan## ########
                if v <= v_temp:
                    v = v_temp
                    transisi = (prev_tag,tag)
                    emistion = (word.rstrip("\n"),tag)
                    choosen_tag = tag
                    if tag_prev == prev_tag:
                        tag_prev_v = v

        
        d_v_prev.update(d_v)
        #print(d_v_prev)
        #prev_v = v
        route.append(choosen_tag)
##########################################
        #print("\n*****************")
        if not loop:
            print("nilai v : {} transisi : {} emisi : {}".format(v,transisi,emistion))
            if tag_prev != transisi[0]:
                print("New route")
                print("nilai v : {} transisi : {} emisi : {}".format(tag_prev_v,(tag_prev,transisi[1]),emistion))
                print("*****************\n")
            else:
                print("*****************\n")
            tag_prev = transisi[1]
    if not loop:
        file_result.close()       
    #print("tag jalur = {}".format(route))
    return route



def Compare(loop,routes,i_ayat):
    f = open("data/dataproses/data_uji_pembanding.csv","r")
    fs = f.readlines()
    f.close()
    list_tag_latih = []

    if not loop:
        ayat_tag = []
        ayat = fs[i_ayat].split("(")
        for word in ayat:
            tag = word.split("=")[1]
            ayat_tag.append(tag.rstrip("\n"))
        list_tag_latih.append(ayat_tag)
        print("tag uji : {}".format(routes[0]))
        print("tag sebenarnya : {}".format(ayat_tag))

    else:   
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
            
            
            if routes[i][j] == list_tag_latih[i][j]:
                t += 1
            else:
                f += 1

            j += 1
        i += 1
    print("benar = {} | salah = {} | akurasi = {}%".format(t,f,round(t/(f+t) * 100)))


if __name__ == "__main__":
    while True:
        print("*********************************")
        print("Apakah file untuk pengujian sudah ada? (seperti data_uji.csv?)")
        print("1.Belum")
        print("2.Sudah")
        print("3.Keluar")
        choose = int(input())
        print()
        if( choose == 1):
            #print("Masukan jumlah kata untuk kalimat yang akan diujikan (saran 10)")
            #param = int(input())
            print("Masukan jumlah kata untuk experimen pada setiap kalimat")
            param2 = int(input())
            param1 = []
            print("Masukan jumlah partisi : ")
            param1.append(int(input()))
            for i in range(0,param1[0]):
                print(str(i+1) + ".Partisi_" + str(i+1))
            print(str(i+2)+".Akhiri")
            while(True):
                val = int(input("Gunakan enter untuk setiap partisi\nMasukan nomor pilihan partisi : "))
                if(val == param1[0]+1):
                    break
                else:
                    param1.append(val)
            start_time = time.time()    
            print("Kamus Probabilitas sedang dibuat harap bersabar")
            list_tag = list(lib.GetUniqueTag(1))
            lib.CreateDictionaryWord()
            lib.CreateDictionaryAyat()
            lib.PartitionData(param1,param2)
            tag_latih_trans,d_trans = lib.Transition()
            d_emition = lib.Emition()
            lib.dict_to_csv(d_trans,"data/dataproses/Transisi")
            lib.dict_to_csv(d_emition,"data/dataproses/Emition")
            print("Kamus sudah dibuat dengan total waktu pengerjaan sebagai berikut")
            PrintTime(time.time() - start_time)
        elif(choose == 2):
            start_time = time.time()  
            tag_latih_trans,d_trans = lib.Transition()
            f = open("data/dataproses/data_uji.csv","r")
            fs = f.readlines()
            f.close()
            print("1.Menguji Akurasi")
            print("2.Menguji Satu Kalimat")
            choose = int(input())
            if(choose == 2):
                print("Masukan nilai indeks \n*Jangan melebihi dari jumlah indeks yang ada pada data_uji.csv (1 - "+str(len(fs)-1)+")")
                choose = int(input())
                routes = []
                route = uji(False,tag_latih_trans,fs[choose - 1])
                routes.append(route)
                Compare(False,routes,choose - 1)
            else:
                print("Tunggu perhitungan akurasi")
                routes = []
                i = 0
                while i < len(fs):
                    route = uji(True,tag_latih_trans,fs[i])
                    i += 1
                    routes.append(route)
                
                Compare(True,routes,choose - 1)
                print("Total waktu pengerjaan Akurasi sebagai berikut")
                PrintTime(time.time() - start_time)
                
            
        else:
            break
