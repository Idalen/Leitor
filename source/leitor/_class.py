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
from .preprocessing import close



class Leitor:

    """
    Main class of the project. It is not finished.
    Everything below is written for testing only
    """

    def __init__(self):
        pass

    def test(self, path):

        path = Path(path)

        image = imageio.imread(path)

        image = grayscaling(image)

        image = gaussian_blur(image, 2, 5)

        image = sharpen(image)

        image = tresholding(image)

        ## not sure of this approach, read README for futher understanding
        # image = erode(image)
        # image = dilate(image)

        image = deskew(image) 

        # horizontal projection (line segmentation)
        #plt.barh(list(range(image.shape[0])),np.sum(image, axis=1))

        plt.imshow(image, cmap='gray')

        plt.show()




