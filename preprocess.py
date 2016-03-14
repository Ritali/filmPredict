import math
import random
import collections

def ReadFile(fileName):
    fi = open(fileName,'r')
    txt = fi.readlines()
    fi.close()
    print "load "+fileName+" data finished !"
    return txt

dict_id = {}
dict_tag = {}
def Handle(txt_input,txt_test, out_input,out_validate,out_test,usermap,filmmap):
    f1 = open(out_input,'w')
    f2 = open(out_validate,'w')
    f3 = open(out_test,"w")
    f_usermap = open(usermap,'w')
    f_filmmap = open(filmmap,'w')


    #dict_tagidf = {}
   
    dict_id_tag = {}
    dict_id = {}
    dict_tag = {}
    id_no = 0
    tag_no = 0

    #input data split to train and validate data
    for line in txt_input:
        line = line.strip()
        items = line.split('\t')

        songid = items[0]
    

        tag = items[1] 
        score = items[2:]

        # if dict_tagidf[tag]<30: #At least 30 songs has this tag
        #     continue
        
        #map build
        if songid not in dict_id:
            dict_id[songid] = id_no
            id_no += 1
        if tag not in dict_tag:
            dict_tag[tag] = tag_no
            tag_no += 1
        
        #every song's tags number
        if songid in dict_id_tag:
            dict_id_tag[songid] += 1
        else:
            dict_id_tag[songid] = 1
        num = dict_id_tag[songid]
        d = dict_id[songid]
        t = dict_tag[tag]
        s = '\t'.join(score)
        if num<=2:#validate
            f2.write(str(d)+'\t'+str(t)+'\t'+s+'\n')
        else:#train
            f1.write(str(d)+'\t'+str(t)+'\t'+s+'\n')


    #test data change to numberic data 
    for line in txt_test:
        line = line.strip()
        items = line.split('\t')
        songid = items[0]
        tag = items[1] 
        if songid not in dict_id:
            dict_id[songid] = id_no
            id_no += 1
        if tag not in dict_tag:
            dict_tag[tag] = tag_no
            tag_no += 1

        d = dict_id[songid]
        t = dict_tag[tag]
        f3.write(str(d)+'\t'+str(t)+'\n')

    #output map
    sort_id = collections.OrderedDict(sorted(dict_id.items(), key=lambda t:t[1], reverse=False))
    for songid in sort_id:
        f_usermap.write(songid+'\t'+str(sort_id[songid])+'\n')
        
    sort_tag = collections.OrderedDict(sorted(dict_tag.items(), key=lambda t:t[1], reverse=False))
    for tag in sort_tag:
        f_filmmap.write(tag+'\t'+str(sort_tag[tag])+'\n')
    
    print "Get svd train and test data done !"
    print "after filter matrix, users %d" %len(dict_id.keys())
    print "after filter matrix, films %d" %len(dict_tag.keys())


def main():
    print "*****************handleInput.py*****************"
    print "Get svd_input, step 3-Filter:Get svd_train and svd_test\n"
    svd_input = 'originalData/input'
    svd_test_input = 'originalData/test'
    songmap = 'idMap/usermap'
    tagmap = 'idMap/filmmap'

    out_svd_train = 'trainData/svd_train'
    out_svd_validate = 'trainData/svd_validate'
    out_svd_test = 'testData/svd_test'

    txt_input = ReadFile(svd_input)
    txt_test = ReadFile(svd_test_input)
    #filter
    Handle(txt_input, txt_test, out_svd_train, out_svd_validate, out_svd_test, songmap, tagmap)

if __name__ == '__main__':
    main()

