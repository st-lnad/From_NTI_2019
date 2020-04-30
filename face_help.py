import cognitive_face as CF
from json import *
import cv2
import os
import sys

trash = open('faceapi.json', 'r')
trsh = load(trash)
KEY = trsh['key']
BASE_URL = trsh['serviceUrl']
grid = trsh['groupId']
trash.close()

CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)
path = os.getcwd() + '/frames/'


# создание директории для временных файлов
def make_dir_fr():
    try:
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    except:
        pass
    os.mkdir(path)


# удаление директории, завершение работы программы
def end():
    try:
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    except:
        pass
    sys.exit(0)


# создает 5 файлов ('frame'+ count +'.jpg', проверяет на наличие 5 лиц)
def get_frames(video):
    cap = cv2.VideoCapture(video)
    fr_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(1, fr_cnt - 1)
    fuck, now_fr = cap.read()
    if not fuck:
        while not fuck:
            fr_cnt -= 1
            cap.set(1, fr_cnt - 1)
            fuck, now_fr = cap.read()
    if fr_cnt < 5:
        print("The video does not follow requirements")
        # Файл person.json не создается.
        end()
    indexes = [0,
               int((fr_cnt - 1) / 4),
               int((fr_cnt - 1) / 2),
               int((fr_cnt - 1) * 3 / 4),
               int(fr_cnt - 1)]
    for i in range(len(indexes)):
        cap.set(1, indexes[i])
        ret, now_fr = cap.read()
        cv2.imwrite(path + 'frame.jpg', now_fr)
        res = CF.face.detect(path + 'frame.jpg')
        if not res:
            print('The video does not follow requirements')
            # Файл person.json не создается.
            end()
        cv2.imwrite(path + 'frame_find_' + str(i) + '.jpg', now_fr)
        fr_cnt += 1


# функция для US-010
def verlorene(video):
    make_dir_fr()
    get_frames(video)
    try:
        CF.person_group.get(grid)
    except:
        print('The service is not ready')
        # Файл person.json не создается.
        end()
    if CF.person_group.get(grid)['userData'] == 'NeedTrain':
        # удаление person.json
        print('The service is not ready')
        try:
            os.remove('person.json')
        except:
            pass
        end()
    li = CF.face.identify([CF.face.detect(path + 'frame_find_0.jpg')[0]['faceId'],
                           CF.face.detect(path + 'frame_find_1.jpg')[0]['faceId'],
                           CF.face.detect(path + 'frame_find_2.jpg')[0]['faceId'],
                           CF.face.detect(path + 'frame_find_3.jpg')[0]['faceId'],
                           CF.face.detect(path + 'frame_find_4.jpg')[0]['faceId']],
                          grid)
    pers = []
    cand = []
    for i in range(5):
        for j in range(len(li[i]['candidates'])):
            if str(li[i]['candidates'][j]['confidence']) >= '0.5':
                cand.append(li[i]['candidates'][j]['personId'])
    cand_set = set(cand)
    if cand_set.__len__() != 1:
        print('The person was not found')
        # Файл person.json не создается.
        end()
    cands = []
    for i in cand_set:
        cands.append(i)
    for i in cands:
        if cand.count(i) == 5:
            pers.append(i)
    if len(pers) == 1:
        # В текущей директории создан файл person.json
        data = {"id": str(pers[0])}
        with open("person.json", "w") as write_file:
            dump(data, write_file)
        print(pers[0] + ' identified')
        end()
    else:
        print('The person was not found')
        # Файл person.json не создается.
        end()

