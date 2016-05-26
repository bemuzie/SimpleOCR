import numpy as np
import os
import matplotlib.pyplot as plt
from skimage import io
import csv

TRAINSET_FOLDER = './train_set'
TRAINSET_data = 'trainset.csv'

with open(TRAINSET_data,'w') as train_data:
    trainwriter = csv.writer(train_data, delimiter=',')
    fig = plt.figure()
    plt.imshow(np.zeros((10,10)))
    plt.show(block=False)
    for f in os.listdir(TRAINSET_FOLDER):
        img = io.imread(os.path.join(TRAINSET_FOLDER,f))
        plt.imshow(img)
        plt.draw()
        value = input('Input number:')
        trainwriter.writerow([f,value])


