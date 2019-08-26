import os
import glob
import cv2


imgs1 = glob.glob(os.path.join('data', 'train', '*', '*.jpg'))
imgs2 = glob.glob(os.path.join('data', 'test', '*', '*.jpg'))
base = (112, 112, 3)
counter = 0
for i in imgs1+imgs2:
    img = cv2.imread(i, cv2.IMREAD_UNCHANGED)

    # get dimensions of image
    dimensions = img.shape
    if base != dimensions:
        counter += 1
        print(i)

    # print('Image Dimension    : ', dimensions)

print(counter)
