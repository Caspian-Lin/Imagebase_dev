import os
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
import numpy as np
import sys, hashlib, sqlite3

def compute_md5(filepath: str) -> str:
    md5_hash = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def get_file_extension(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    return [file_name, file_extension]

def SSMI(img1, img2): #
    ssmi = img1+img2
    return ssmi

testfilepath="C:/Users/28491/OneDrive - Xi'an Jiaotong-Liverpool University/Lab/Imagebase_dev/testimg\\illust_114543923_20240106_005217.jpg"

# 加载图像并进行预处理 
img_path = testfilepath
if get_file_extension(img_path)[-1] not in [".jpg",".png"]:
    print("文件类型不受支持，程序终止")
    sys.exit()
filename = img_path.split('\\')[-1]
# 算哈希
md5_value = compute_md5(img_path)
print(f"MD5 hash of {filename}: {md5_value}")
# 加载VGG16模型
vgg16 = VGG16(weights='imagenet', include_top=True)
# 提取特征
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)
features = vgg16.predict(img_array)

# 存进SQL
conn = sqlite3.connect('testdatabase.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS main (hash,filename,filepath,feature)
''')
cursor.execute(f'''
    INSERT INTO main (hash,filename,filepath,feature) 
               VALUES (?,?,?,?);''', (md5_value,filename,img_path,features))


# 打印每一行
cursor.execute("SELECT * FROM main")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.commit()
conn.close()
