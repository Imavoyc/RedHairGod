import sys
import os

original_data_dir  = 'data'
text_cn_dir = 'text_cn'
out_dir = 'data_out'

def refine_text(txt):
    if '艾格妮斯' in txt:
        txt = txt.replace('艾格妮斯','艾格妮丝' )
    return txt
    
def import_text(file):
    new_json = ''
    chs_db = {}
    cur_pos = 0
    
    forig = open(os.path.join(original_data_dir,file),"r", encoding = "utf-8")
    old_json = forig.read()
    forig.close()

    txt_filename = os.path.basename(file)
    txt_filename = os.path.splitext(txt_filename)[0] + '.txt'
    ftxt = open(os.path.join(text_cn_dir,txt_filename),"r", encoding = "utf-8")
    txt_lines = ftxt.readlines()
    ftxt.close()
    for line in txt_lines:
        if line.startswith('◆'):
            p = int(line[1:7])
            chs = line[8:].strip()
            chs_db[p] = refine_text(chs)


    chs_list = list(chs_db.keys())
    chs_list.sort()

    for k in chs_list:
        assert(k > cur_pos)
        assert(old_json[k-1] == '"')
        
        if(old_json[k-20:k].rfind('characterName') != -1):
            continue
            
        if(old_json[k-50:k].rfind('"code":356') != -1):
            continue
        if(old_json[k-30:k].rfind('"code":41') != -1):
            continue
        if(old_json[k-40:k].rfind('"code":322') != -1):
            continue
        if(old_json[k-50:k].rfind('"code":250') != -1):
            continue
        if(old_json[k-50:k].rfind('"code":245') != -1):
            continue
        new_json = new_json + old_json[cur_pos:k]
        new_json = new_json + chs_db[k]
        cur_pos = old_json.index('"',k)
        
        #
        #p1 = k - 1
        #p2 = old_json.index('"',k) + 1
        #print('222' + old_json[k:cur_pos])

    new_json = new_json + old_json[cur_pos:]
    fout = forig = open(os.path.join(out_dir,file),"w", encoding = "utf-8")
    fout.write(new_json)
    fout.close()
import_text(sys.argv[1])