import datetime
import os
from .config import LOG_DIRECTORY

def make_imagelog_dir(module_name):
    now = datetime.datetime.now()
    folder_name = now.strftime('%Y_%m_%d/%H_%M_%S')
    log_dir = os.path.join(LOG_DIRECTORY, module_name, folder_name)

    # 디렉토리 이름에 접미사 추가를 위한 카운터
    counter = 1

    # 접미사가 추가된 디렉토리 경로
    unique_log_dir = log_dir

    # 이미 해당 디렉토리가 존재하면, 접미사(_1, _2, ...)를 추가하여 유일한 이름 생성
    while os.path.exists(unique_log_dir):
        unique_log_dir = f"{log_dir}_{counter}"
        counter += 1

    # 유일한 디렉토리 생성
    os.makedirs(unique_log_dir)

    return unique_log_dir

def make_image_folder(module_name):
    log_dir = os.path.join(LOG_DIRECTORY, module_name)

    return log_dir