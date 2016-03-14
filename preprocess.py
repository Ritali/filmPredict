import math
import random
import collections

splitString = '::'
dict_id = {}
dict_tag = {}

def ReadFile(fileName):
    fi = open(fileName,'r')
    txt = fi.readlines()
    fi.close()
    print "load "+fileName+" data finished !"
    return txt

#calculate the overall average
def Average(fileName):
    #fi = open(fileName, 'r')
    #print fileName
    result = 0.0
    cnt = 0
    for line in fileName:
        cnt += 1
        arr = line.split()
        #result += int(arr[2].strip())
        #print arr[0],arr[1]
        result += float(arr[2].strip())
    #print cnt
    return result / cnt
    #return result / N

def ConfUpdate(conf_file, svd_train):
    print "update conf with train data"
    f = open(conf_file,'w')
    # 3.579596041 3706 50 0.01 0.05
    # averageScore userNum itemNum factorNum learnRate regularization 
    
    avg = Average(ReadFile(svd_train))

    print("average score of train data is %f" %avg)

    userNum = len(dict_id.keys())
    filmNum = len(dict_tag.keys())
    factorNum = 50
    learnRate = 0.01
    regularization = 0.05
    
    firstline = str(avg) + " " + str(userNum) + " " + str(filmNum) + " " + str(factorNum) + " " + str(learnRate) + " " + str(regularization)

    f.write(firstline+"\n")
    f.write("averageScore userNum itemNum factorNum learnRate regularization\n")
    print "conf file updated !"


def Handle(txt_input,txt_test, out_input,out_validate,out_test,usermap,filmmap):
    print "preprocess train and test data"
    f1 = open(out_input,'w')
    f2 = open(out_validate,'w')
    f3 = open(out_test,"w")
    f_usermap = open(usermap,'w')
    f_filmmap = open(filmmap,'w')


    #dict_tagidf = {}
   
    dict_id_tag = {}
    
    id_no = 0
    tag_no = 0

    #input data split to train and validate data
    for line in txt_input:
        line = line.strip()
        items = line.split(splitString)
        if len(items)<3:
            continue
        userid = items[0]

        filmid = items[1] 
        #print filmid
        score = items[2]

        # if dict_tagidf[tag]<30: #At least 30 songs has this tag
        #     continue
        
        #map build
        if userid not in dict_id:
            dict_id[userid] = id_no
            id_no += 1
        if filmid not in dict_tag:
            dict_tag[filmid] = tag_no
            tag_no += 1
        
        #every song's tags number
        if userid in dict_id_tag:
            dict_id_tag[userid] += 1
        else:
            dict_id_tag[userid] = 1
        num = dict_id_tag[userid]
        d = dict_id[userid]
        t = dict_tag[filmid]
        s = '\t'.join(score)
        if num<=2:#validate
            f2.write(str(d)+'\t'+str(t)+'\t'+s+'\n')
        else:#train
            f1.write(str(d)+'\t'+str(t)+'\t'+s+'\n')


    #test data change to numberic data 
    for line in txt_test:
        line = line.strip()
        items = line.split(splitString)
        userid = items[0]
        filmid = items[1] 
        if userid not in dict_id:
            dict_id[userid] = id_no
            id_no += 1
        if filmid not in dict_tag:
            dict_tag[filmid] = tag_no
            tag_no += 1

        d = dict_id[userid]
        t = dict_tag[filmid]
        f3.write(str(d)+'\t'+str(t)+'\n')

    #output map
    sort_id = collections.OrderedDict(sorted(dict_id.items(), key=lambda t:t[1], reverse=False))
    for songid in sort_id:
        f_usermap.write(songid+'\t'+str(sort_id[songid])+'\n')
        
    sort_tag = collections.OrderedDict(sorted(dict_tag.items(), key=lambda t:t[1], reverse=False))
    for tag in sort_tag:
        f_filmmap.write(tag+'\t'+str(sort_tag[tag])+'\n')
    
    print "get svd train and test data done !"
    print "after filter matrix, users %d" %len(dict_id.keys())
    print "after filter matrix, films %d" %len(dict_tag.keys())


def main():
    print "*****************handleInput.py*****************"
    print "Get svd_input, step 3-Filter:Get svd_train and svd_test\n"
    svd_input = 'originalData/movie/ratings.dat'
    svd_test_input = 'originalData/movie/test.dat'
    
    # svd_input = 'originalData/input'
    # svd_test_input = 'originalData/test'

    songmap = 'idMap/usermap'
    tagmap = 'idMap/filmmap'

    out_svd_train = 'trainData/svd_train'
    out_svd_validate = 'trainData/svd_validate'
    out_svd_test = 'testData/svd_test'
    conf_file = "conf/svd.conf"

    txt_input = ReadFile(svd_input)
    txt_test = ReadFile(svd_test_input)

    #filter
    Handle(txt_input, txt_test, out_svd_train, out_svd_validate, out_svd_test, songmap, tagmap)
    #conf file update
    ConfUpdate(conf_file, out_svd_train)
    

if __name__ == '__main__':
    main()

