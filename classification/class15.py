import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, Activation,Dropout,Conv2D, MaxPooling2D,BatchNormalization, Flatten
from tensorflow.keras.optimizers import Adam, Adamax
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras import regularizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model, load_model, Sequential
import numpy as np
import pandas as pd
import shutil
import time
import cv2 as cv2
# from tqdm import tqdm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import os
# import seaborn as sns
# sns.set_style('darkgrid')
# from PIL import Image
from sklearn.metrics import confusion_matrix, classification_report
# from IPython.core.display import display, HTML
# stop annoying tensorflow warning messages
import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

def predictor(sdir, csv_path, model_path, crop_image = False):
    print('@@ predictor')
    # read in the csv file
    class_df=pd.read_csv(csv_path)
    img_height=int(class_df['height'].iloc[0])
    img_width =int(class_df['width'].iloc[0])
    img_size=(img_width, img_height)
    scale=class_df['scale by'].iloc[0]
    try:
        s=int(scale)
        s2=1
        s1=0
    except:
        split=scale.split('-')
        s1=float(split[1])
        s2=float(split[0].split('*')[1])
        print (s1,s2)
    path_list=[]
    paths=os.listdir(sdir)
    for f in paths:
        path_list.append(os.path.join(sdir,f))
    print (' Model is being loaded- this will take about 10 seconds')
    model=load_model(model_path)
    image_count=len(path_list)
    index_list=[]
    prob_list=[]
    cropped_image_list=[]
    result_p = []
    class_names = []
    pros= []
    idxes = []
    good_image_count=0
    for i in range (image_count):
        img=cv2.imread(path_list[i])
        # img = cv2.imread(path_list[i], cv2.IMREAD_REDUCED_COLOR_2)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if crop_image:
            # status, img=crop(img)
            status, img = img.crop(10,10,300,300)
        else:
            status=True
        if status:
            good_image_count +=1
            img=cv2.resize(img, img_size)
            cropped_image_list.append(img)
            img=img*s2 - s1
            img=np.expand_dims(img, axis=0)
            p= np.squeeze (model.predict(img))
            result_p = p
            index=np.argmax(p)
            prob=p[index]
            index_list.append(index)
            prob_list.append(prob)

    if good_image_count == 1:
        class_name= class_df['class'].iloc[index_list[0]]
        probability= prob_list[0]
        img=cropped_image_list[0]
#         plt.title(class_name, color='blue', fontsize=16)
#         plt.axis('off')
#         plt.imshow(img)
        for idx, val in enumerate(result_p):
            # 30% 이상
            # if val >= 0.3:
            # 80% 이상, 240118
            if val >= 0.8:
                idxes.append(idx)
                class_names.append(class_df['class'].iloc[idx])
                pros.append(val)

        # print('class_names :', type(class_names), class_names)
        # print('pros :',type(pros),pros)
        # print('result_p :', type(result_p), result_p)
        return idxes, class_names, pros, result_p
    else:
        return None, None, None
#     most=0
#     for i in range (len(index_list)-1):
#         key= index_list[i]
#         keycount=0
#         for j in range (i+1, len(index_list)):
#             nkey= index_list[j]
#             if nkey == key:
#                 keycount +=1
#         if keycount> most:
#             most=keycount
#             isave=i
#     best_index=index_list[isave]
#     psum=0
#     bestsum=0
#     for i in range (len(index_list)):
#         psum += prob_list[i]
#         if index_list[i]==best_index:
#             bestsum += prob_list[i]
#     img= cropped_image_list[isave]/255
#     class_name=class_df['class'].iloc[best_index]
# #     plt.title(class_name, color='blue', fontsize=16)
# #     plt.axis('off')
# #     plt.imshow(img)
#     return class_name, bestsum/image_count

