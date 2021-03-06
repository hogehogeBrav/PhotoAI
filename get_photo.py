import os
import glob
import csv
import pykakasi
from PIL import Image
from value import *


kakasi = pykakasi.kakasi()

WIDTH = 256
HEIGHT = 144

folder_dir = './'
result_hepburn = []

def get_photo(folder_dir , value_list):
  for value_name in value_list:
    conv = kakasi.convert(value_name)
    hepburn_name = conv[0]['hepburn']
    result_hepburn.append(hepburn_name)
    
    from icrawler.builtin import BingImageCrawler
    crawler = BingImageCrawler(storage={"root_dir": os.path.join(folder_dir , 'photos/' , value_name)})
    crawler.crawl(keyword=value_name , max_num=250)

    dir_name = os.path.join(folder_dir , 'photos/' ,value_name)
    new_dir_name = os.path.join(folder_dir , 'resize/' , hepburn_name)
    if not os.path.exists(new_dir_name):
        os.makedirs(new_dir_name)

    for file in os.listdir(dir_name):
        base, ext = os.path.splitext(file)
        if ext == '.jpg':
            print(file)
            #画像の元データを開く
            img = Image.open(os.path.join(dir_name, file))
            # img = Image.open(os.path.join(dir_name, file)).convert('RGB').save(os.path.join(dir_name, file))
            #画像を2分の1に縮小
            img_resize = img.resize(size=(WIDTH, HEIGHT))
            #縮小した画像を別フォルダに保存
            img_resize.save(os.path.join(new_dir_name, file))

  with open('value_list.csv' , 'w') as f:
    writer = csv.writer(f,lineterminator="\n")
    writer.writerow(result_hepburn)
            
get_photo(folder_dir , value_list)