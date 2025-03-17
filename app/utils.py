from PIL import Image
import os
# Logger
import logging
logger = logging.getLogger(__name__)

def image_preprocessing(img_array, filename):
    extension = os.path.splitext(filename)[1]

    if extension.lower() == ".jpg" or extension.lower() == ".jpeg":
        # Exif 데이터 가져오기
        exif = img_array._getexif()

        # Exif 데이터가 있으면 orientation 정보 출력
        if exif is not None:
            # orientation의 Exif 태그는 274
            orientation = exif.get(274)
            logger.info("Orientation:" + str(orientation))

            # 이미지를 적절히 회전합니다.
            if orientation == 3:
                img_array = img_array.rotate(180, expand=True)
            elif orientation == 6:
                img_array = img_array.rotate(270, expand=True)
            elif orientation == 8:
                img_array = img_array.rotate(90, expand=True)
        else:
            print("No Exif data.")
    else:
        print("Not a JPEG file.")

    if img_array.mode == "RGBA":
        # alpha 채널 제거
        r, g, b, a = img_array.split()
        img_array = Image.merge("RGB", (r, g, b))

    print(img_array.size)
    max_size = (1920,1920)
    img_array.thumbnail(max_size)
    print(img_array.size)

    return img_array


def crop_with_expansion(image, box, expand_ratio):
    # Calculate the expanded box coordinates
    x1, y1, x2, y2 = box
    expand_w = int((x2 - x1) * expand_ratio)
    expand_h = int((y2 - y1) * expand_ratio)

    # Calculate expanded box coordinates with boundary checks
    expanded_x1 = max(0, x1 - expand_w)
    expanded_y1 = max(0, y1 - expand_h)
    expanded_x2 = min(image.width - 1, x2 + expand_w)
    expanded_y2 = min(image.height - 1, y2 + expand_h)
    expanded_box = (expanded_x1, expanded_y1, expanded_x2, expanded_y2)

    # Crop the detected area from the original image using the expanded box
    cropped_img = image.crop(expanded_box)
    return cropped_img