import random
import os
import glob


train_data = 'train_data'
test_data = 'test_data'
dataset_path = '../../Data_Set/'
id_path = 'id_path'
train_percent = 80


def id():
    id_name = {}
    entries = os.listdir(dataset_path)

    try:
        os.remove(id_path)
    except OSError:
        pass

    id_path_file = open(id_path, 'w+')

    for i, folder in enumerate(entries):
        id_path_file.write(str(i+1)+' '+folder+'\n')
        id_name[folder] = str(i+1)

    id_path_file.close()
    print('Add %d id' % (len(entries)))
    print('Done!')
    return id_name


def rename():
    entries = os.listdir(dataset_path)
    counter = 0
    for i, folder in enumerate(entries):
        videos = glob.glob(os.path.join(dataset_path, folder, '*.mp4'))
        for j in videos:
            counter += 1
            os.rename(j, os.path.join(dataset_path,
                                      folder, folder+'_'+j.split('/')[-1]))

    print('Rename %d file' % (counter))
    print('Done!!')


def type(percent):
    return random.randrange(100) > percent


# def get_lists():
#     train_data_file = open(train_data, 'r+')
#     test_data_file = open(test_data, 'r+')

#     train_data_list = train_data_file.read().split('\n')
#     test_data_list = test_data_file.read().split('\n')

#     train_data_list = train_data_list[0:len(train_data_list)-1]
#     test_data_list = test_data_list[0:len(test_data_list)-1]

#     return train_data_list, test_data_list


def make_lists(id_name):
    entries = os.listdir(dataset_path)

    try:
        os.remove(train_data)
    except OSError:
        pass

    try:
        os.remove(test_data)
    except OSError:
        pass

    train_data_file = open(train_data, 'w+')
    test_data_file = open(test_data, 'w+')

    for i, folder in enumerate(entries):
        videos = glob.glob(os.path.join(dataset_path, folder, '*.mp4'))

        if len(videos) > 1:
            for j in videos:
                if type(train_percent):
                    test_data_file.write(j.replace(dataset_path, '')+'\n')
                else:
                    train_data_file.write(
                        j.replace(dataset_path, '') + ' ' + id_name[folder] + '\n')
        else:
            train_data_file.write(videos[0].replace(
                dataset_path, '') + ' ' + id_name[folder] + '\n')

    train_data_file.close()
    test_data_file.close()

    print('Make train and test list')
    print('Done!!!')


def move():
    entries = os.listdir(dataset_path)
    counter = 0
    for i, folder in enumerate(entries):
        videos = glob.glob(os.path.join(dataset_path, folder, '*.mp4'))
        for j in videos:
            counter += 1
            os.rename(j,  j.split('/')[-1])

    print('Move %d file' % (counter))
    print('Done!!')


def main():
    id_name = id()
    rename()
    make_lists(id_name)
    move()


if __name__ == "__main__":
    main()
