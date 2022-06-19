import imageio
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
 
from .preprocessing import gaussian_blur
from .preprocessing import grayscaling
from .preprocessing import tresholding
from .preprocessing import deskew
from .preprocessing import dilate
from .preprocessing import erode
from .preprocessing import sharpen

class Leitor:

    def __init__(self):
        pass

    def test(self, path):

        path = Path(path)

        image = imageio.imread(path)

        image = grayscaling(image)

        image = gaussian_blur(image, 2, 5)
  
        image = sharpen(image)

        image = tresholding(image)

        image = erode(image)

        image = dilate(image)   

        plt.imshow(image, cmap='gray')   


        plt.show()



