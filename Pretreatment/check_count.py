import json
import shutil
import os


def readJson(input_path):
    img_ori =[i for i in os.listdir(input_path)]
    with open('instances_test2021.json', 'r', encoding='UTF8') as f:
        json_data = json.load(f)
    images = [i['file_name'] for i in json_data['images']]

    print(len(img_ori))
    print(len(images))