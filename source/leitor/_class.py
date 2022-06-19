import imageio
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from PIL import Image
import tempfile

 
from .preprocessing import gaussian_blur
from .preprocessing import grayscaling
from .preprocessing import tresholding
from .preprocessing import deskew
from .preprocessing import dilate
from .preprocessing import erode
from .preprocessing import sharpen
from .preprocessing import close


class Leitor:

    def __init__(self):
        pass

    def test(self, path):

        path = Path(path)

        #path = self._set_image_dpi(path)

        image = imageio.imread(path)

        image = grayscaling(image)


        image = gaussian_blur(image, 2, 5)

        image = sharpen(image)

        image = tresholding(image)

        plt.subplot(121)
        plt.title("Binarized Image")
        plt.imshow(image, cmap='gray')  
        #imageio.imwrite('tresholding_image_nopp.png',image,) 

        image = erode(image)

        image = dilate(image)

        plt.subplot(122)
        plt.title("Eroded and Dilated Image")
        plt.imshow(image, cmap='gray')

        #imageio.imwrite('tresholding_image_nopp.png',image,)   


        
        plt.show()


    # def _set_image_dpi(self, file_path):
    #     im = Image.open(file_path)
    #     image_size = 1000
    #     length_x, width_y = im.size
    #     factor = max(1, int(image_size / length_x))
    #     size = factor * length_x, factor * width_y
    #     # size = (1800, 1800)
    #     im_resized = im.resize(size, Image.ANTIALIAS)
    #     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    #     temp_filename = temp_file.name
    #     im_rotated = im_resized.rotate(270, Image.NEAREST, expand = 1)
    #     im_rotated.save(temp_filename, dpi=(300, 300))
    #     return temp_filename



