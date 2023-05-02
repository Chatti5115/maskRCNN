import os
import json
from collections import Counter

class validation:
    def __init__(self):
        print('다운로드 받은 파일의 경로를 입력하세요')
        self.path = input('json: ')
        self.obj_list_1 = ['도로균열', '도로(홀)']
        self.result ={}
        self.count = 0
        self.read_folder(self.path)
        self.getResult()

    def read_folder(self, path):
        file_list = os.listdir(path)
        for file_ in file_list:
            file_ = os.path.join(path, file_)
            if os.path.isdir(file_):
                self.read_folder(file_)
            if '.json' in file_:
                self.count += 1
                print(file_)
                self.result = Counter(self.result) + Counter(self.readJson(file_))
                print(self.count)

    def readJson(self, json_f):
        result = {}
        img_len = 0
        data = dict(
            categories=[
                # supercategory, id, name
            ],
            label=[],
            tag={
                'polygon': 0,
            }
        )
        if '.json' in json_f:
            with open(json_f, 'r', encoding='UTF8') as f:
                json_data = json.load(f)
            labels = [i['name'] for i in json_data['categories']]
            for i in labels:
                i = i.encode('utf-8').decode('utf-8')
                data["categories"].append(
                    dict(id=labels.index(i) + 1, name=i)
                )
            image = [i['image_id'] for i in json_data['annotations']]
            img_len = len(list(set(image)))
            category = [i['category_id'] for i in json_data['annotations']]
            for i in category:
                data["label"].append(i)
            result = self.getCount(data)
            result['total_사진'] = img_len
            return result

    def getCount(self, data_):
        test = {label: 0 for label in self.obj_list_1}
        for i in data_['categories']: #모든 라벨
            test[i['name']] =data_['label'].count(i['id'])
        return test

    def getResult(self):
        for i in self.obj_list_1:
            if i not in self.result.keys():
                self.result[i] = 0
        print(self.result)



validation()
os.system('pause')