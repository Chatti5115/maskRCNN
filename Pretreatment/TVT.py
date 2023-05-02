import os
import shutil
class getFile():
    def __init__(self):
        self.input_path = input('path: ')
        self.count =0
        self.img_list = []

        self.train =[]
        self.valid =[]
        self.test =[]
        self.getImage(self.input_path)
        self.getImage('case2_json')
        self.divide()

    def getImage(self, input_path):
        file_list = [os.path.join(input_path, i) for i in os.listdir(input_path)]
        for file in file_list:
            if os.path.isdir(file) :
                self.getImage(file)
            elif ".json" in file:
                self.count+=1
                print(self.count)
                self.img_list.append(file.split('\\')[-1])

    def divide(self):
        self.img_list = list(set(self.img_list))
        train =[]
        valid =[]
        self.img_list.sort()
        for i in self.img_list:
            print(i)
            if len(train) < 8:
                train.append(os.path.join(self.input_path, i))
            elif len(train) == 8:
                if len(valid) == 0:
                    valid.append(os.path.join(self.input_path, i))
                    # print(self.img_list.index(i))
                elif len(valid) == 1:
                    self.train.extend(train)
                    self.valid.extend(valid)
                    self.test.append(os.path.join(self.input_path, i))
                    # print(self.img_list.index(i))
                    train = []
                    valid =[]
            # if self.img_list.index(i) == len(self.img_list)-1:
            if self.img_list.index(i) == len(self.img_list)-1:
                if len(train) != 0:
                    self.train.extend(train)
        self.move_img()

    def move_img(self):
        train_dir = 'E:\\case2_원본데이터\\data_upload\\train'
        valid_dir ='E:\\case2_원본데이터\\data_upload\\valid'
        test_dir = 'E:\\case2_원본데이터\\data_upload\\test'

        for file in self.train:
            file_path= file.replace(file.split('\\')[-1],'')
            file= file.split('\\')[-1]

            if file.split('_')[5][0] == '0':
                if file.split('_')[5][1] == '0':
                    rename = file.split('_')[5].replace('00', '')
                    file = file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2] + '_' + file.split('_')[3] + '_' + file.split('_')[4] + '_' + file.split('_')[5].replace(file.split('_')[5], rename) + '_' + file.split('_')[6]
                else:
                    file = file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2] + '_' + file.split('_')[3] + '_' + file.split('_')[4] + '_' + file.split('_')[5][1:] + '_' + file.split('_')[6]
            if os.path.isfile(os.path.join(file_path,file)):
                shutil.copy(os.path.join(file_path,file),train_dir)
            else:
                shutil.copy(os.path.join('E:\\case2_원본데이터\\case2_json',file),train_dir)

        print(len(self.valid))
        for file in self.valid:
            file_path= file.replace(file.split('\\')[-1],'')
            file= file.split('\\')[-1]
            if file.split('_')[5][0] == '0':
                if file.split('_')[5][1] == '0':
                    rename = file.split('_')[5].replace('00', '')
                    file = file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2] + '_' + file.split('_')[3] + '_' + file.split('_')[4] + '_' + file.split('_')[5].replace(file.split('_')[5], rename) + '_' + file.split('_')[6]
                    # file = file.replace('_00', '_')
                else:
                    file = file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2] + '_' + file.split('_')[3] + '_' + file.split('_')[4] + '_' + file.split('_')[5][1:] + '_' + file.split('_')[6]
            print(file)
            if os.path.isfile(os.path.join(file_path,file)):
                shutil.copy(os.path.join(file_path,file),valid_dir)
            else:
                shutil.copy(os.path.join('E:\\case2_원본데이터\\case2_json',file),valid_dir)

        print(len(self.test))
        for file in self.test:
            file_path= file.replace(file.split('\\')[-1],'')
            file= file.split('\\')[-1]
            if file.split('_')[5][0] == '0':
                if file.split('_')[5][1] == '0':
                    # file = file.replace('_00', '_')
                    rename = file.split('_')[5].replace('00', '')
                    file = file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2] + '_' + file.split('_')[3] + '_' + file.split('_')[4] + '_' + file.split('_')[5].replace(file.split('_')[5], rename) + '_' + file.split('_')[6]
                else:
                    file = file.split('_')[0] + '_' + file.split('_')[1] + '_' + file.split('_')[2] + '_' + file.split('_')[3] + '_' + file.split('_')[4] + '_' + file.split('_')[5][1:] + '_' + file.split('_')[6]
            print(file)
            if os.path.isfile(os.path.join(file_path,file)):
                shutil.copy(os.path.join(file_path,file),test_dir)
            else:
                shutil.copy(os.path.join('E:\\case2_원본데이터\\case2_json',file),test_dir)



getFile()