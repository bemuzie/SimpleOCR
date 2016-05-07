from skimage import io
import numpy as np
from skimage import filters
from skimage import morphology
from skimage import measure
from matplotlib import pyplot as plt
import csv

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class

class Input_image():
    def __init__(self,image_path):
        self.image = io.imread(image_path)
        self.text_colors = ()
    def read_roi(self,path_to_roilist):
        self.rois = AutoVivification()
        with open(path_to_roilist,'r') as roilist_file:
            csvreader = csv.DictReader(roilist_file)
            for row in csvreader:
                self.rois[row['region_name']][row['roi_name']]['x_min'] = int(row['x_min'])
                self.rois[row['region_name']][row['roi_name']]['y_min'] = int(row['y_min'])
                self.rois[row['region_name']][row['roi_name']]['x_max'] = int(row['x_max'])
                self.rois[row['region_name']][row['roi_name']]['y_max'] = int(row['y_max'])

    def batch_process(self,func,input_label,output_label,**kwargs):
        for region_name, region_dict in self.rois.items():
            for roi_name, roi_dict in region_dict.items():
                self.rois[region_name][roi_name][label] = func(**kwargs)

    def crop_image(self):
        for region_name,region_dict in self.rois.items():
            for roi_name,roi_dict in region_dict.items():
                self.rois[region_name][roi_name]['image'] = self.image[roi_dict['y_min']:roi_dict['y_max'],
                                                                       roi_dict['x_min']:roi_dict['x_max']
                                                                      ]
    def show_image(self):
        plt.imshow(self.image[...,1])
        plt.show()
    def preprocess(self,image=None):
        if image is None:
            image = self.image
        image_processed = np.zeros(image.shape[:-1])
        for rgb in self.text_colors:
            image_processed [ (image[...,0] == rgb[0]) &
                                   (image[...,1] == rgb[1]) &
                                   (image[...,2] == rgb[2])
                                   ] = 1
        return image_processed

    def add_text_color(self,r,g,b):
        self.text_colors += ((r,g,b),)

    def segment(self):
        self.bw = self.image_processed
        self.label_image = measure.label(self.bw)




if __name__ == '__main__':
    plt.interactive(False)


    test_image = './test_image/N1.png'
    test = input_image(test_image)
    test.add_text_color(0,238,238)
    test.add_text_color(153, 153, 153)
    test.add_text_color(255, 255, 255)
    test.add_text_color(255, 255, 0)
    test.read_roi('./roi_list.csv')
    test.crop_image()
    for i in test.rois.values():
        for ii in i.values():
            plt.imshow(ii['image'], interpolation='none' )
            plt.show()


