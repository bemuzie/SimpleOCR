import os
from skimage import io
import numpy as np
from skimage import filters
from skimage import morphology
from skimage import transform
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

class Screenshot():
    def __init__(self,image_path):
        self.base_name = os.path.basename(image_path).split('.')[0]
        self.image = io.imread(image_path)
        self.text_colors = ()
    def _sanitize_colors(self, color_str):
        list_of_colors = color_str.split(';')
        colors_final = []
        for color in list_of_colors:
            out_colour = color.replace('(','').replace(')','').split(',')
            out_colour = [int(i) for i in out_colour]
            colors_final.append(out_colour )
        return colors_final


    def read_roi(self, path_to_roilist):
        self.rois = AutoVivification()
        with open(path_to_roilist, 'r') as roilist_file:
            csvreader = csv.DictReader(roilist_file)
            for row in csvreader:
                self.rois[row['region_name']][row['roi_name']]['x_min'] = int(row['x_min'])
                self.rois[row['region_name']][row['roi_name']]['y_min'] = int(row['y_min'])
                self.rois[row['region_name']][row['roi_name']]['x_max'] = int(row['x_max'])
                self.rois[row['region_name']][row['roi_name']]['y_max'] = int(row['y_max'])
                self.rois[row['region_name']][row['roi_name']]['color'] = self._sanitize_colors(row['roi_colors'])

    def crop_image(self):
        for region_name, region_dict in self.rois.items():
            for roi_name, roi_dict in region_dict.items():
                self.rois[region_name][roi_name]['image'] = Image(self.image[roi_dict['y_min']:roi_dict['y_max'],
                                                                       roi_dict['x_min']:roi_dict['x_max']
                                                                      ])
                self.rois[region_name][roi_name]['image'].add_text_colors(self.rois[region_name][roi_name]['color'])
                self.rois[region_name][roi_name]['image'].preprocess()
                self.rois[region_name][roi_name]['image'].segment()
                #self.rois[region_name][roi_name]['image'].show_characters()

    def save_characters(self,out_folder):
        for region_name, region_dict in self.rois.items():
            for roi_name, roi_dict in region_dict.items():
                for i, im in enumerate(self.rois[region_name][roi_name]['image'].characters):
                    plt.imshow(im,interpolation='none')
                    plt.savefig('%s/%s_%s_%s_%s.png'%(out_folder,self.base_name,region_name,roi_name,i) )




class Image():
    def __init__(self,image):
        self.image = image
        self.text_colors = []
        self.characters = []
    def show_image(self):
        plt.imshow(self.image)
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
        self.image = image_processed

    def add_text_color(self,r,g,b):
        self.text_colors += ((r,g,b),)
    def add_text_colors(self, rgb):
        self.text_colors += rgb
    def segment(self,margin=0):
        self.bw = self.image
        self.image = measure.label(self.bw, connectivity=1)
        for region in measure.regionprops(self.image):
            if (region.bbox[2] - region.bbox[0] >2 and region.bbox[3]-region.bbox[1] >2):
                character_image = self.image[region.bbox[0]-margin:region.bbox[2]+margin,
                                             region.bbox[1]-margin:region.bbox[3]+margin]
                character_image[character_image!=region.label] = 0


                self.characters.append(character_image)
    def resize_characters(self,x=10,y=10):
        for i in self.characters:
            resized = transform.resize(np.array(i,dtype=float), (x,y))


    def show_characters(self):
        plot_size = len(self.characters)
        for i in range(plot_size):
            plt.subplot(1,plot_size,i+1)

            plt.imshow(self.characters[i])
        plt.show()






if __name__ == '__main__':
    plt.interactive(False)

    for image in os.listdir('/media/10E5-CC88/PYATKIN D.A'):
        test = Screenshot('/media/10E5-CC88/PYATKIN D.A/'+image)
        test.read_roi('./roi_list.csv')
        test.crop_image()
        test.save_characters('./train_set')

