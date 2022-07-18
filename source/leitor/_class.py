import imageio
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import os
import shutil
from tqdm import tqdm
 
from .preprocessing import gaussian_blur
from .preprocessing import grayscaling
from .preprocessing import tresholding
from .preprocessing import deskew
from .preprocessing import dilate
from .preprocessing import erode
from .preprocessing import sharpen
from .preprocessing import binary_inv

from .line_segmentation import segment_lines



class Leitor:

    """
    Main class of the project. It is not finished.
    Everything below is written for testing only
    """

    def __init__(self):
        pass

    def extract(self, path, save=None):
        
        path = Path(path)
        image = imageio.imread(path)

        if save:
            save = Path(save) 
            if save.is_dir:
                shutil.rmtree(save)
            os.makedirs(save)

        preprocessed_image = self.preprocess(image, save)

        seg_lines, seg_image = segment_lines(preprocessed_image)

        if save:
            imageio.imwrite(save/'segemented_img.png', seg_image)
            for i in range(len(seg_lines)):
                imageio.imwrite(save/f'segmented_line_{i}.png', seg_lines[i])
        
        
 

    def preprocess(self, image, save):

        greyscaled_image = grayscaling(image)

        filtered_image = gaussian_blur(greyscaled_image, 2, 5)

        sharpened_image = sharpen(filtered_image)

        binary_image = tresholding(sharpened_image)

        ## not sure of this approach, read README for futher understanding
        morphfiltered_image = erode(binary_image)
        morphfiltered_image = dilate(morphfiltered_image)

        deskewed_image = deskew(morphfiltered_image) 

        preprocessed_image = binary_inv(deskewed_image)


        if save:
            imageio.imwrite(save/'original_image.png', image)
            imageio.imwrite(save/'greyscaled_image.png', greyscaled_image.astype('uint8'))
            imageio.imwrite(save/'filtered_image.png', filtered_image.astype('uint8'))
            imageio.imwrite(save/'sharpened_image.png', sharpened_image.astype('uint8'))
            imageio.imwrite(save/'binary_image.png', binary_image.astype('uint8'))
            imageio.imwrite(save/'morphfiltered_image.png', morphfiltered_image.astype('uint8'))
            imageio.imwrite(save/'deskewed_image.png', deskewed_image.astype('uint8'))
            imageio.imwrite(save/'preprocessed_image.png', preprocessed_image.astype('uint8'))


        return preprocessed_image


    def load(self, dir):
        self.dir = Path(dir)
        self.files = [self.dir/file for file in os.listdir(self.dir) if not (self.dir/file).is_dir()]

    def process_save(self):
        
        output_dir = self.dir.parent/'mask'
        os.makedirs(output_dir, exist_ok=True)

        for path in tqdm(self.files):
                image = self.open(path=path).astype("float64")
                image /= np.max(image)
                imageio.imwrite(output_dir/path.name, image.astype("int8"))

    def open(self, path=None, index=0):
        if path == None:
            image = imageio.imread(self.files[index])
        else:
            image = imageio.imread(path)

        return image


    




