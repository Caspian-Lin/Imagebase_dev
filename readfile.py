import sqlite3, os

def refresh_all_files_under_dir():
    entires =[]
    for root,dirs,files in os.walk(directory):
        for file in files:
            entires.append(os.path.join(root, file))
    return entires

def read_jpg_metadata(imgpath):
    mdata_b = open(imgpath,"rb").read()
    mdata_h = mdata_b.hex()
    return mdata_h

directory = "C://Users//28491//OneDrive - Xi'an Jiaotong-Liverpool University//Lab//Imagebase_dev//testimg"
testfilepath="testimg/illust_114543923_20240106_005217.jpg"

print(read_jpg_metadata(testfilepath))