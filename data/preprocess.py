"""
After extracting the RAR, we run this to move all the files into
the appropriate train/test folders.

Should only run this file once!
"""
import os
import os.path
import random
import os
import glob
import csv
from subprocess import call


train_data = 'train_data'
test_data = 'test_data'
dataset_path = '../../lrs/'
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


def get_train_test_lists(version='01'):
    """
    Using one of the train/test files (01, 02, or 03), get the filename
    breakdowns we'll later use to move everything.
    """
    # Get our files based on version.
    # test_file = os.path.join('ucfTrainTestlist', 'testlist' + version + '.txt')
    # train_file = os.path.join(
    #     'ucfTrainTestlist', 'trainlist' + version + '.txt')

    # Build the test list.
    with open(test_data) as fin:
        test_list = [row.strip() for row in list(fin)]

    # Build the train list. Extra step to remove the class index.
    with open(train_data) as fin:
        train_list = [row.strip() for row in list(fin)]
        train_list = [row.split(' ')[0] for row in train_list]

    # Set the groups in a dictionary.
    file_groups = {
        'train': train_list,
        'test': test_list
    }

    return file_groups


def move_files(file_groups):
    """
    This assumes all of our files are currently in _this_ directory.
    So move them to the appropriate spot. Only needs to happen once.
    """
    # Do each of our groups.
    for group, videos in file_groups.items():

        # Do each of our videos.
        for video in videos:

            # Get the parts.
            parts = video.split(os.path.sep)
            classname = parts[0]
            filename = parts[1]

            # Check if this class exists.
            if not os.path.exists(os.path.join(group, classname)):
                print("Creating folder for %s/%s" % (group, classname))
                os.makedirs(os.path.join(group, classname))

            # Check if we have already moved this file, or at least that it
            # exists to move.
            if not os.path.exists(filename):
                print("Can't find %s to move. Skipping." % (filename))
                continue

            # Move it.
            dest = os.path.join(group, classname, filename)
            print("Moving %s to %s" % (filename, dest))
            os.rename(filename, dest)

    print("Done.")


def extract_files():
    """After we have all of our videos split between train and test, and
    all nested within folders representing their classes, we need to
    make a data file that we can reference when training our RNN(s).
    This will let us keep track of image sequences and other parts
    of the training process.

    We'll first need to extract images from each of the videos. We'll
    need to record the following data in the file:

    [train|test], class, filename, nb frames

    Extracting can be done with ffmpeg:
    `ffmpeg -i video.mpg image-%04d.jpg`
    """
    data_file = []
    folders = ['train', 'test']

    for folder in folders:
        class_folders = glob.glob(os.path.join(folder, '*'))

        for vid_class in class_folders:
            class_files = glob.glob(os.path.join(vid_class, '*.mp4'))

            for video_path in class_files:
                # Get the parts of the file.
                video_parts = get_video_parts(video_path)

                train_or_test, classname, filename_no_ext, filename = video_parts

                # Only extract if we haven't done it yet. Otherwise, just get
                # the info.
                if not check_already_extracted(video_parts):
                    # Now extract it.
                    src = os.path.join(train_or_test, classname, filename)
                    dest = os.path.join(train_or_test, classname,
                                        filename_no_ext + '-%04d.jpg')
                    call(["ffmpeg", "-i", src, dest])

                # Now get how many frames it is.
                nb_frames = get_nb_frames_for_video(video_parts)

                data_file.append(
                    [train_or_test, classname, filename_no_ext, nb_frames])

                print("Generated %d frames for %s" %
                      (nb_frames, filename_no_ext))

    with open('data_file.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(data_file)

    print("Extracted and wrote %d video files." % (len(data_file)))


def get_nb_frames_for_video(video_parts):
    """Given video parts of an (assumed) already extracted video, return
    the number of frames that were extracted."""
    train_or_test, classname, filename_no_ext, _ = video_parts
    generated_files = glob.glob(os.path.join(train_or_test, classname,
                                             filename_no_ext + '*.jpg'))
    return len(generated_files)


def get_video_parts(video_path):
    """Given a full path to a video, return its parts."""
    parts = video_path.split(os.path.sep)
    filename = parts[2]
    filename_no_ext = filename.split('.')[0]
    classname = parts[1]
    train_or_test = parts[0]

    return train_or_test, classname, filename_no_ext, filename


def check_already_extracted(video_parts):
    """Check to see if we created the -0001 frame of this file."""
    train_or_test, classname, filename_no_ext, _ = video_parts
    return bool(os.path.exists(os.path.join(train_or_test, classname,
                                            filename_no_ext + '-0001.jpg')))


def main():

    id_name = id()
    rename()
    make_lists(id_name)
    move()

    """
    Go through each of our train/test text files and move the videos
    to the right place.
    """
    # Get the videos in groups so we can move them.
    group_lists = get_train_test_lists()
    # print(group_lists)

    # Move the files.
    move_files(group_lists)

    """
    Extract images from videos and build a new file that we
    can use as our data input file. It can have format:

    [train|test], class, filename, nb frames
    """
    extract_files()


if __name__ == '__main__':
    main()
