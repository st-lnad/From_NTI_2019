import cognitive_face as CF
from json import load
import cv2
import os
import sys
import argparse
import time

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
    cap.set(1, fr_cnt-1)
    fuck, now_fr = cap.read()
    if not fuck:
        while not fuck:
            fr_cnt -= 1
            cap.set(1, fr_cnt - 1)
            fuck, now_fr = cap.read()
    if fr_cnt < 5:
        print('Video does not contain any face')
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
            print('Video does not contain any face')
            end()
        cv2.imwrite(path + 'frame' + str(i) + '.jpg', now_fr)
        fr_cnt += 1


# US-004 Простое добавление пользователя в сервис индентификации
# sample-add
def my_simple_add(video):
    make_dir_fr()
    get_frames(video)
    try:
        CF.person_group.create(grid)
    except:
        pass
    CF.person_group.update(grid, user_data='NeedTrain')
    res = CF.person.create(grid, 'id')['personId']
    print('5 frames extracted')
    print('PersonId:', res)
    print('FaceIds')
    print('=======')
    for i in range(5):
        print(CF.person.add_face(path + 'frame' + str(i) + '.jpg', grid, res)['persistedFaceId'])
    end()


# US-005 Улучшенное добавление пользователя в сервис индентификации
# add
def clever_add(video1, video2, video3, video4, video5):
    # Функция не реализована из-за высокой сложности в условиях нехватки временени.
    # По условию мы должны проверить 5 видео за 2 минуты.
    # Мы решили заставить работать приложение в 5 потоков, но написать распознавание видео и многопоточку не успели.
    pass


# US-006 Получение всех пользователей из сервиса идентификации
# list
def list():
    try:
        li = CF.person.lists(grid)
        if len(li) == 0:
            print('No persons found')
        else:
            print('Persons IDs:')
            for i in li:
                print(i['personId'])
    except:
        print('The group does not exist')
    sys.exit(0)


# US-007 Удаление пользователя из сервиса идентификации
# del
def my_delete(prid):
    try:
        CF.person.lists(grid)
    except:
        print("The group does not exist")
        sys.exit(0)
    try:
        CF.person.delete(grid,prid)
        CF.person_group.update(grid, user_data='NeedTrain')
        print('Person deleted')
    except:
        print("The person does not exist")
    sys.exit(0)


# US-008 Запуск обучения сервиса индентификации
# train
def my_crazy_train():
    try:
        CF.person_group.get(grid)
    except:
        print('There is nothing to train')  # проверка на существование группы
        sys.exit(0)

    if not CF.person.lists(grid):
        print('There is nothing to train')  # проверка на наличие пользователей в группе
        sys.exit(0)
    if (CF.person_group.get(grid)['userData'] == 'NeedTrain') or (CF.person_group.get(grid)['userData'] is None):
        CF.person_group.train(grid)
        CF.person_group.update(grid, user_data='no')
        print('Training successfully started')
    else:
        print('Already trained')
    sys.exit(0)


# парсер
def key_to_value(args):
    if args.simple_add != " ":
        my_simple_add(args.simple_add)
    if args.add != " ":
        clever_add(args.add[0], args.add[1], args.add[2], args.add[3], args.add[4])
    if args.list != " ":
        list()
    if args.delete != " ":
        my_delete(args.delete)
    if args.train != " ":
        my_crazy_train()


parser = argparse.ArgumentParser()
parser.add_argument('--simple-add', default=' ', nargs='?')
parser.add_argument('--add', default=' ', nargs='+')
parser.add_argument('--list', default=' ', nargs='?')
parser.add_argument('--delete', '-d', default=' ', nargs='?')
parser.add_argument('--train', default=' ', nargs='?')
parser.set_defaults(func=key_to_value)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
