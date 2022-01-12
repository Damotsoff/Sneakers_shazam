import os
from api.image_processing import crop_image, get_data
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from operator import itemgetter

DARKNET_PATH = "/home/jabulani/Final_Project/bot/api/darknet/"


class BashmakModel:
    def __init__(self, input_image: str) -> None:
        self.input_image = input_image
        self.image_file = "/home/jabulani/Final_Project/bot/api/image_file.txt"
        self.result_path = "/home/jabulani/Final_Project/bot/api/result.txt"

        with open(self.image_file, 'w') as f:
            f.write(self.input_image)

    def get_yolo_prediction(self) -> None:
        os.system(f"{DARKNET_PATH}darknet detector test {DARKNET_PATH}data/obj.data {DARKNET_PATH}cfg/custom-yolov4-detector.cfg {DARKNET_PATH}backup/custom-yolov4-detector_best-2.weights -thresh 0.8 -dont_show -ext_output <{self.image_file}> {self.result_path}")

    def yolo_image_processing(self, output_image) -> None:
        result_dict = get_data(self.result_path)

        for image_name, coords in result_dict.items():
            crop_image(image_name, coords[0], output_image)

    def get_resnet_prediction(self, processed_image):
        train_generator_classes = {
            'Adidas_NMD_R1': 0,
            'Adidas_Ultra_Boost_4.0': 1,
            'Adidas_Yeezy_Boost_350': 2,
            'Adidas_Yeezy_Boost_700': 3,
            'Air_Jordan_11': 4,
            'Air_Jordan_12': 5,
            'Air_Jordan_13': 6,
            'Air_Jordan_1_Retro_High': 7,
            'Air_Jordan_4': 8,
            'Air_Jordan_6': 9,
            'Nike_Air_Force_1_Low': 10,
            'Nike_Air_Huarache': 11,
            'Nike_Air_Max_1': 12,
            'Nike_Air_Max_90': 13,
            'Nike_Air_Max_95': 14,
            'Nike_Air_VaporMax': 15,
            'Nike_Blazer': 16,
            'Nike_Dunk_low': 17,
            'Reebok_Instapump_Fury': 18,
            'Unknown': 19
        }

        model = load_model('/home/jabulani/Final_Project/bot/api/checkpoint')
        
        img = image.load_img(processed_image, target_size=(224, 224))

        x = image.img_to_array(img).astype('float32') / 255
        x = np.expand_dims(x, axis=0)

        preds = model.predict(x)
        sorted_preds = list(reversed(np.argsort(preds, axis=1)[:, -4:][0]))

        labels = list(train_generator_classes.keys())
        selector = itemgetter(*sorted_preds)
        return selector(labels)
