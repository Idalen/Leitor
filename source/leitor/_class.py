import imageio
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import os
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

    def extract(self, path):
        
        path = Path(path)
        image = imageio.imread(path)

        preprocessed_image = self.preprocess(image)

        seg_lines, seg_image = segment_lines(preprocessed_image)

        # plt.subplot(121)
        # plt.imshow(preprocessed_image, cmap='gray')
        # plt.subplot(122)
        plt.imshow(seg_image, cmap='gray')
        plt.show()
 

    def preprocess(self, image):

        image = grayscaling(image)

        image = gaussian_blur(image, 2, 5)

        image = sharpen(image)

        image = tresholding(image)

        ## not sure of this approach, read README for futher understanding
        image = erode(image)
        image = dilate(image)

        image = deskew(image) 

        image = binary_inv(image)

        return image


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


    




