import math
import random
import collections

def ReadFile(fileName):
    fi = open(fileName,'r')
    txt = fi.readlines()
    fi.close()
    print "load "+fileName+" data finished !"
    return txt

def LoadMap(txt_map):
    dict = {}
    for line in txt_map:
        line = line.strip()
        items = line.split('\t')
        no = items[1]
        item = items[0]
        dict[no] = item
    return dict
    
def PreOut(txt,out,songmap,tagmap):
    f = open(out,'w')
    word_list = []
    
    for line in txt:
        line = line.strip()
        items = line.split('\t')
        song_no = items[0]
        
        tags_pre = items[1:]
        num = 0
        str_out = []
        if song_no in songmap:
            song_id = songmap[song_no]# song_no in songmap
            str_out.append(song_id)

        for t in tags_pre:
            if num%2 == 0:
                tag_no = t # tag_no in tagmap 
                if tag_no in tagmap:
                    tag_name = tagmap[tag_no]
                    str_out.append(tag_name)
            else:
                tag_score = t # tag_score in prediction
            num += 1
        str_r = '\t'.join(str_out)
        if str_r:
            f.write(str_r+'\n')
    print "predicted films output finished !"


def main():

    pre_file = 'predict/svd_input_prediction'
    songmap = 'idMap/usermap'
    tagmap = 'idMap/filmmap'
    out = 'predict/result'

    txt_pre = ReadFile(pre_file)
    txt_song = ReadFile(songmap)
    txt_tag = ReadFile(tagmap)
    songmap_dict = LoadMap(txt_song)
    tagmap_dict = LoadMap(txt_tag)

    PreOut(txt_pre,out,songmap_dict,tagmap_dict)

if __name__ == '__main__':
    main()


