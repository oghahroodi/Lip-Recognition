import csv
from __future__ import print_function
import os
import plaidml.keras
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"


def get_data():
    """Load our data from file."""
    with open(os.path.join('data', 'data_file.csv'), 'r') as fin:
        reader = csv.reader(fin)
        data = list(reader)

    return data


def split_train_test():
    """Split the data into train and test groups."""
    train = []
    test = []
    for item in data:
        if item[0] == 'train':
            train.append(item)
        else:
            test.append(item)
    return train, test


x_train = []
y_train = []
x_test = []
y_test = []


data = get_data()
train, test = split_train_test()

# print(train)
for i in train:
    print(i)
