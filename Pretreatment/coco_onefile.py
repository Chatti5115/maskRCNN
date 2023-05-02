import datetime
import os
import json

import numpy as np
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class onefile :
    def __init__(self):
        now = datetime.datetime.now()
        self.path = input('annotations: ')

        self.polygon_label = ['경계석', '측구', '맨홀', '중앙분리대', 'PE 방호벽', '임시 안전방호벽']

        self.polygon_train = dict(
            info=dict(
                description=None,
                url=None,
                version=None,
                year=now.year,
                contributor=None,
                date_created=now.strftime("%Y-%m-%d %H:%M:%S.%f"),
            ),
            licenses=[dict(url=None, id=1, name=None, )],
            images=[
                # license, url, file_name, height, width, date_captured, id
            ],
            type="instances",
            annotations=[
                # segmentation, area, iscrowd, image_id, bbox, category_id, id
            ],
            categories=[
                # supercategory, id, name

            ],
        )

        self.writeLabel(self.polygon_label, self.polygon_train)
        self.getJson_f(self.path)

    def writeLabel(self, list, dictionary):
        for label in list:
            print(label)
            if label == '경계석':
                dictionary["categories"].append(
                    dict(supercategory=None, id=list.index(label)+1, name='border_stone'))
            if label == '측구':
                dictionary["categories"].append(
                    dict(supercategory=None, id=list.index(label)+1, name='side_sphere'))
            if label == '맨홀':
                dictionary["categories"].append(
                    dict(supercategory=None, id=list.index(label)+1, name='manhole'))
            if label == '중앙분리대':
                dictionary["categories"].append(
                    dict(supercategory=None, id=list.index(label)+1, name='center_separato'))
            if label == 'PE 방호벽':
                dictionary["categories"].append(
                    dict(supercategory=None, id=list.index(label)+1, name='PE_barrier'))
            if label == '임시 안전방호벽':
                dictionary["categories"].append(
                    dict(supercategory=None, id=list.index(label)+1, name='temporary_safety_barrier'))

    def getJson_f(self, path):
        file_list = os.listdir(path)
        for file_ in file_list:
            file_ = os.path.join(path, file_)
            if os.path.isdir(file_):
                self.getJson_f(file_)
            else:
                if '.json' in file_:
                    print(file_)
                    self.readJson(file_)
        self.getImage()
        self.jsonWrite()



    def readJson(self, j_file):
        label_dict = {}
        image_dict = {}
        with open(j_file, 'r', encoding='UTF8') as f:
            json_data = json.load(f)
        anno = [i for i in json_data['annotations']]
        category = [i for i in json_data['categories']]
        image = [i for i in json_data['images']]

        for img in image:
            image_dict[img['id']] = img['file_name']

        for category_name in category:
            if category_name['name'] in self.polygon_label:
                label_dict[category_name['id']] = category_name['name']
        for label in anno:
            if label['category_id'] in label_dict.keys():
                #box 객체 segmentation 추가
                if len(label['segmentation']) == 0:
                    label['segmentation'] = [[label['bbox'][0], label['bbox'][1], label['bbox'][0]+label['bbox'][2], label['bbox'][1],
                                         label['bbox'][0]+label['bbox'][2], label['bbox'][1]+label['bbox'][3], label['bbox'][0], label['bbox'][1]+label['bbox'][3]]]
                self.polygon_train["annotations"].append(
                    dict(
                        id=len(self.polygon_train["annotations"])+1,
                        image_id=image_dict[label['image_id']],
                        category_id=label_dict[label['category_id']],
                        segmentation=label['segmentation'],
                        area=label['area'],
                        bbox=label['bbox'],
                        iscrowd=0,
                    )
                )

    def getImage(self):
        total_anno = [i for i in self.polygon_train['annotations']]
        total_image= list(set([i['image_id'] for i in total_anno]))
        for img in total_image:
            self.polygon_train["images"].append(
                dict(
                    license=0,
                    url=None,
                    file_name=img,
                    height=1080,
                    width=1920,
                    date_captured=None,
                    id=len(self.polygon_train['images'])+1
                )
            )
        img_dict ={}
        total_img = [i for i in self.polygon_train['images']]
        for i in total_img:
            img_dict[i['file_name']] = i['id']
        label_dict ={}
        total_label = [i for i in self.polygon_train['categories']]
        for i in total_label:
            label_dict[i['name']] = i['id']

        for i in total_anno:
            if i['category_id'] =='경계석':
                i['category_id'] = 'border_stone'
            if i['category_id'] == '측구':
                i['category_id'] = 'side_sphere'
            if i['category_id'] == '맨홀':
                i['category_id'] = 'manhole'
            if i['category_id'] == '중앙분리대':
                i['category_id'] = 'center_separato'
            if i['category_id'] == 'PE 방호벽':
                i['category_id'] = 'PE_barrier'
            if i['category_id'] == '임시 안전방호벽':
                i['category_id'] = 'temporary_safety_barrier'
            i['category_id'] = label_dict[i['category_id']]
            i['image_id'] = img_dict[i['image_id']]


    def jsonWrite(self):
        file_name = 'case2_valid.json'
        print('write file: ' + file_name)
        with open(file_name, "w", encoding='UTF8') as f:
            json.dump(self.polygon_train, f, ensure_ascii=False, cls=NumpyEncoder)


if __name__ == "__main__":
    onefile()



