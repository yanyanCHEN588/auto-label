# -*- coding: utf-8 -*-
"""
2021-10-29
@author: yan

將基礎人工過濾好的，並且也有在過濾過程中補或是修正label YOLO format
1.將被淘汰的，不管是json or xml 格式 重複也沒差， 不予複製至新資料夾
2.將僅有txt (YOLO)的複製至新資料夾

[#]複製目的地 "s" 對拉 目前同層
        dst_imgpath = 'check'+'/'+i+'.jpg'
        dst_txtpath = 'check'+'/'+i+'.txt'


"""
#%% load module
from pathlib import Path
import os
import shutil

#%%json coco
###-----------config----------

os.chdir(os.path.dirname(__file__))
# filterpath=Path("Extension-block_Obj365")
labelformat = 'txt'
img_dir='images' 
anno_dir='labels'

# cls="Microwave" 

# allpath=filterpath/"ALL_Extention Cord_len_377.txt"
#讀取ALL.txt清單 一開始創立的


# %%讀取xml檔名並存檔與計算數量
del_list=[]
for xml in Path(anno_dir).glob('*.xml'):
    del_list.append(xml.name[:-4])


# %%讀取json檔名並存檔與計算數量
chg_list=[]
for xml in Path(anno_dir).glob('*.json'):
    chg_list.append(xml.name[:-5])

#%% SAV = ALL - DEL -CHG

all_list=[]
for xml in Path(anno_dir).glob('*.txt'):
    all_list.append(xml.name[:-4])


for i in all_list:
    if (i not in del_list) and (i not in chg_list):
        img_path=img_dir+'/'+i+'.jpg'
        txt_path=anno_dir+'/'+i+'.txt'
        dst_imgpath = 'check'+'/'+i+'.jpg'
        dst_txtpath = 'check'+'/'+i+'.txt'
        shutil.copy(img_path, dst_imgpath)#複製貼上影像
        shutil.copy(txt_path, dst_txtpath)#複製貼上影像


# %%
