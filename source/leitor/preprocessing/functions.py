from math import degrees
import numpy as np
import cv2

from ..utils import convolution2d
from ..utils import normalize


def gaussian_blur(image, k, sigma):
    
    """
    Applies a gaussian blur to an image
    
    parameters:
        image - numpy.array
            the image to be degraded by the gaussian blur
        k - int
            The size of the degradation function
        sigma - int
            A optimizable constant
    output:
        numpy.ndarray
            The image with gaussian blur
    """

    #computes gaussian degradation function
    arx = np.arange((-k // 2) + 1.0, (k // 2) + 1.0)
    x, y = np.meshgrid(arx, arx)
    filt = np.exp(-(1/2) * (np.square(x) + np.square(y)) / np.square(sigma))
    degradation_function = filt / np.sum(filt)
    
    
    #pads degradation function to apply convolution
    a = int(image.shape[0]//2 - degradation_function.shape[0]//2)
    b = int(image.shape[1]//2 - degradation_function.shape[1]//2)
    degradation_function = np.pad(degradation_function, ((a,a),(b,b)), 'constant', constant_values=(0))

    # #transforms the matrix into frequency domain
    # F_image = np.fft.fft2(image)
    # F_degradation_function = np.fft.fft2(degradation_function, s=image.shape)

    # #computes degraded image
    # degraded_image = (np.abs(np.fft.fftshift(np.fft.ifft2(F_image*F_degradation_function))))

    degraded_image = convolution2d(image, degradation_function)

    return normalize(degraded_image)

def grayscaling(image):
    return image[:, :, 0]

def tresholding(image, window_size=3):
    
    ####TODO code it in julia

    # pad_width = window_size//2
    # padded_image = np.pad(image, pad_width, mode='edge')

    # new_image = np.zeros(image.shape)

    # for i in range(pad_width, padded_image.shape[0]-pad_width):
    #     for j in range(pad_width, padded_image.shape[1]-pad_width):
    #         treshold = np.mean(padded_image[i-window_size//2:ceil(i+window_size/2), j-window_size//2:ceil(j+window_size/2)])
    #         new_image[i-pad_width, j-pad_width] = padded_image[i, j] > treshold

    new_image = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 21, np.mean(image) // 4)

    return new_image


def deskew(image):

    dilate = cv2.dilate(image, np.ones((15,2)), iterations=3)

    edges = cv2.Canny(dilate, 50, 150, apertureSize=3)
    
    ''' Finds the skew angle of an edge image by repeatedly
        applying the hough lines algorithm '''

    (h, w) = edges.shape[:2]
    threshold = max(h, w)
    while True:
        #print('Testing with treshold', threshold)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)

        if lines is None or len(lines) == 0:
            threshold -= threshold // 4
            continue

        angles = []
        for line in lines:
            for rho, theta in line:
                angle = (theta - np.pi / 2.0)
                angle = degrees(angle) % 360
                if angle > 180:
                    angle = angle - 360
                # Ignores angles not in the -60 to 60 range
                if angle > 60 or angle < -60:
                    continue
                angles.append(angle)
        if not len(angles):
            # Reduces the threshold until we find at least some lines
            threshold -= threshold // 4
            continue
        break
    # Calculate the average of the line's angles
    angle = np.mean(angles)

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    image = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255)
    
    return image

    

def dilate(image):
    kernel = np.ones((2,2)).astype("uint8")
    new_image = cv2.dilate(image, kernel, iterations=1)

    return new_image

def erode(image):
    kernel = np.array([[1,0,], [0, 1]]).astype(np.uint8)
    new_image = cv2.erode(image, kernel, iterations=1)
    
    return new_image

def close(image):
    kernel = np.ones((2,2)).astype("uint8")
    new_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    return new_image

def sharpen(image):
    """"Laplacian filter"""
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    return cv2.filter2D(image, -1, kernel)