import sys
import os
import shutil
current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

'''local'''
# classification_dir = os.path.join(current_dir, "classification")
'''docker'''
classification_dir = os.path.join(current_dir, "../classification")
sys.path.append(classification_dir)

# 15 -> 12
# from class15 import predictor
from class12 import predictor

# from classification.class15 import predictor
from flask import Flask, request, send_file, jsonify, render_template
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
# from utils import image_preprocessing, crop_with_expansion
from datetime import datetime
import json
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename

'''local'''
# log_dir = os.path.join(current_dir, "log_config")
# sys.path.append(current_dir)
'''docker'''
log_dir = os.path.join(current_dir, "../log_config")
sys.path.append(log_dir)

# Logger
from log_config import enable_additional_logging, disable_additional_logging, make_imagelog_dir, make_image_folder
# from config15 import enable_additional_logging, disable_additional_logging
# from utils15 import make_imagelog_dir

import logging
logger = logging.getLogger(__name__)

import cv2 as cv2

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

'''local'''
# csv_path = '../classification/class_dict.csv'
# model_path = '../classification/model/EfficientNetB4-skin disease-86.21_15class.h5'
'''docker'''
csv_path = 'classification/class_dict.csv'
# model_path = 'classification/model/EfficientNetB4-skin disease-86.21_15class.h5'
model_path = 'classification/model/EfficientNetB4-skin disease-90.09_12class.h5'

app = Flask(__name__)

def skin_check(path):
    # print('@@ skin_check')
    img = cv2.imread(path)

    img_yCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    # lower = np.array([0,133,80], dtype = np.uint8)
    # upper = np.array([255,173,120], dtype = np.uint8)

    skin_msk = cv2.inRange(img_yCrCb, lower, upper)
    # skin = cv2.bitwise_and(img, img, mask=skin_msk)

    tot = skin_msk.shape[0] * skin_msk.shape[1]
    temp_msk = skin_msk / 255
    result = temp_msk.sum()/tot
    print('@@ skin_check :', result)
    logger.info(f"@@ skin_check : [{result}]")
    return temp_msk.sum()/tot


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/classification", methods=["POST"])
def skin_disease_classification():
    # 이미지 파일 저장

    TAG = 'SKIN_DISEASE'
    RESULT_IMAGE_PATH = make_imagelog_dir(TAG)
    STORE_IMAGE_PATH = make_image_folder(TAG)

    workerID = os.getpid()

    enable_additional_logging(RESULT_IMAGE_PATH, __name__)
    try:
        logger.info(f"[{TAG}] [{workerID}] {TAG} detection & recognition process")

        if "image" in request.files:
            image_file = request.files["image"]
            print('@@ INPUT image_file :', type(image_file), image_file)
            logger.info(f"[{TAG}] [{workerID}] @@ INPUT 이미지 : [{image_file}]")

            filename = image_file.filename
            try:
                extension = filename.split(".")[1]
            except:
                logger.info(f"[{TAG}] [{workerID}] 이미지 확장자를 찾을 수 없습니다.")
                response_data = {"error": "이미지 확장자를 찾을 수 없습니다."}
                return jsonify(response_data), 400

            filename = 'image.' + extension

            logger.info(f"[{TAG}] [{workerID}] filename : {filename}")
            print(f"[{TAG}] [{workerID}] filename : {filename}")

            store_path = os.path.join(RESULT_IMAGE_PATH, 'INPUT')
            createDirectory(store_path)
            image_save_path = os.path.join(store_path, filename)
            image_file.save(image_save_path)

            if skin_check(image_save_path) < 0.5:
                logger.info(f"[{TAG}] [{workerID}] 환부를 확대하여 다시 촬영해 주세요.")
                response_data = {"error": "환부를 확대하여 다시 촬영해 주세요."}
                return jsonify(response_data), 400

            idx, label, pro, res_arr = predictor(store_path, csv_path, model_path, crop_image = False)
            res_arr=str(res_arr).replace('\n','')
            res_json = {"index": str(idx), "label": str(label), "probability": str(pro), "res_pro": res_arr}
            print('res_json:', res_json)
            logger.info(f"[{TAG}] [{workerID}] res_json : [{res_json}]")

            # 80% 이상인 피부질환이 없을 때
            if len(idx) == 0:
                logger.info(f"[{TAG}] [{workerID}] 80% 이상인 피부질환이 없습니다.")
                print(f"[{TAG}] [{workerID}] 80% 이상인 피부질환이 없습니다.")
                response_data = {"info": "80% 이상인 피부질환이 없습니다.", "res_pro": res_arr}
                return jsonify(response_data)

            # 분류된 피부질환 save
            for idx, val in enumerate(label):
                label_path = os.path.join(RESULT_IMAGE_PATH, val)
                createDirectory(label_path)
                label_img_path = os.path.join(label_path, filename)
                shutil.copyfile(image_save_path, label_img_path)

                logger.info(f"[{TAG}] [{workerID}] label_img_path : [{label_img_path}]")
                print(f"[{TAG}] [{workerID}] label_img_path : [{label_img_path}]")

                logger.debug(f"[{TAG}] [{workerID}] Result : {res_json}")
                print(f"[{TAG}] [{workerID}] Result : {res_json}")
                with open(os.path.join(label_path, filename + '.json'), 'w', encoding="utf-8") as f:
                    json.dump(res_json, f, indent=4, ensure_ascii=False)  # 4 spaces for indentation

                # label 폴더 별로 save (재학습 대비)
                if pro[idx] >= 0.8:
                    temp_path = os.path.join(STORE_IMAGE_PATH, val)
                    createDirectory(temp_path)
                    temp_name = str(len(os.listdir(temp_path))) + '.' + extension
                    store_path = os.path.join(STORE_IMAGE_PATH, val, temp_name)
                    shutil.copyfile(image_save_path, store_path)

                    logger.debug(f"[{TAG}] [{workerID}] probability 80% 이상인 image store_path : {store_path}")
                    print(f"[{TAG}] [{workerID}] probability 80% 이상인 image store_path : {store_path}")

            logger.info(f"[{TAG}] [{workerID}] Done")
            return jsonify(res_json)
        else:
            logger.info(f"[{TAG}] [{workerID}] 이미지를 찾을 수 없습니다.")
            response_data = {"error": "이미지를 찾을 수 없습니다."}
            return jsonify(response_data), 400
    finally:
        disable_additional_logging(__name__)

# if __name__ == "__main__":
#    app.run(threaded=True, host='0.0.0.0', port=5502, debug=True)
