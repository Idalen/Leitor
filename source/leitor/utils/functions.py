import numpy as np

def convolution2d(a, b):
    A = np.fft.fft2(a)
    B = np.fft.fft2(b, s=a.shape)

    new_image = (np.abs(np.fft.fftshift(np.fft.ifft2(A*B))))

    return new_image

def normalize(img, norm_min=0, norm_max=(2**8)-1):

    """
    Normalize the values in the matrix
    
    parameters:
        img     - numpy.array
            the matrix which will be normalized
        norm_min   - integer
            the minimum value after normalization 
        norm_max   - integer
            the maximum value after normalization 
    output:
        img     - numpy.array
            the matrix normalized
    """

    max_val = np.max(img)
    min_val = np.min(img)

    img = (norm_max-norm_min)*((img - min_val)/(max_val - min_val)) + norm_min 

    return img.astype("uint8")