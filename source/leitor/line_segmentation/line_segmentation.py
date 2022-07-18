
import torch
from torch import nn

from pathlib import Path
import numpy as np # linear algebra
import cv2

MODEL_PATH = Path("../models/line_segmentation.pt")


class Unet(nn.Module):

    def __init__(self):
        super(Unet, self).__init__()
            
        self.conv1 = nn.Conv2d(1, 64, 3, padding='same')
        self.conv2 = nn.Conv2d(64, 64, 3, padding='same')
        self.pool1  = nn.MaxPool2d((2,2))
            
        self.conv3 = nn.Conv2d(64, 128, 3, padding='same')
        self.conv4 = nn.Conv2d(128, 128, 3, padding='same')
        self.pool2  = nn.MaxPool2d((2,2))
            
        self.conv5 = nn.Conv2d(128, 256, 3, padding='same')
        self.conv6 = nn.Conv2d(256, 256, 3, padding='same')
        self.pool3  = nn.MaxPool2d((2,2))
            
        self.conv7 = nn.Conv2d(256, 512, 3, padding='same')
        self.conv8 = nn.Conv2d(512, 512, 3, padding='same')
        self.dropout1 = nn.Dropout(0.5)
        self.pool4 = nn.MaxPool2d((2,2))
            
        self.conv9 = nn.Conv2d(512, 1024, 3, padding='same')
        self.conv10 = nn.Conv2d(1024, 1024, 3, padding='same')
        self.dropout2 = nn.Dropout(0.5)
                   
        self.conv11 = nn.Conv2d(1024, 512, 2, padding='same')
        self.conv12 = nn.Conv2d(1024, 512, 3, padding='same')
        self.conv13 = nn.Conv2d(512, 512, 3, padding='same')
        
        self.conv14 = nn.Conv2d(512, 256, 2, padding='same')
        self.conv15 = nn.Conv2d(512, 256, 3, padding='same')
        self.conv16 = nn.Conv2d(256, 256, 3, padding='same')

        self.conv17 = nn.Conv2d(256, 128, 2, padding='same')
        self.conv18 = nn.Conv2d(256, 128, 3, padding='same')
        self.conv19 = nn.Conv2d(128, 128, 3, padding='same')

        self.conv20 = nn.Conv2d(128, 64, 2, padding='same')
        self.conv21 = nn.Conv2d(128, 64, 3, padding='same')
        self.conv22 = nn.Conv2d(64, 64, 3, padding='same')

        self.conv23 = nn.Conv2d(64, 2, 3, padding='same')
        
        self.conv24 = nn.Conv2d(2, 1, 1, padding='same')
        
        self.merge = lambda x,y : torch.cat((x, y), 1)
        self.upsample = nn.Upsample(scale_factor=2)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid() 
            
            
    def forward(self, x):
        
        inputs = x
        
        conv1 = self.relu(self.conv1(inputs))
        conv2 = self.relu(self.conv2(conv1))
        pool1 = self.pool1(conv2)
        
        conv3 = self.relu(self.conv3(pool1))
        conv4 = self.relu(self.conv4(conv3))
        pool2 = self.pool2(conv4)
        
        conv5 = self.relu(self.conv5(pool2))
        conv6 = self.relu(self.conv6(conv5))
        pool3 = self.pool3(conv6)
        
        conv7 = self.relu(self.conv7(pool3))
        conv8 = self.relu(self.conv8(conv7))
        drop1 = self.dropout1(conv8)
        pool4 = self.pool4(drop1)

        conv9 = self.relu(self.conv9(pool4))
        conv10 = self.relu(self.conv10(conv9))
        drop2 = self.dropout2(conv10)
        
        conv11 = self.relu(self.conv11(self.upsample(drop2)))
        merge1 = self.merge(drop1, conv11)
        conv12 = self.relu(self.conv12(merge1))
        conv13 = self.relu(self.conv13(conv12))
        
        conv14 = self.relu(self.conv14(self.upsample(conv13)))
        merge2 = self.merge(conv6, conv14)
        conv15  = self.relu(self.conv15(merge2))
        conv16  = self.relu(self.conv16(conv15))
        
        conv17 = self.relu(self.conv17(self.upsample(conv16)))
        merge3 = self.merge(conv4, conv17)
        conv18 = self.relu(self.conv18(merge3))
        conv19 = self.relu(self.conv19(conv18))
        
        conv20 = self.relu(self.conv20(self.upsample(conv19)))
        merge4 = self.merge(conv2, conv20)
        conv21 = self.relu(self.conv21(merge4))
        conv22 = self.relu(self.conv22(conv21))
        
        conv23 = self.relu(self.conv23(conv22))
        
        output = self.sigmoid(self.conv24(conv23))
                
        return output

model = Unet()
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))


def segment_lines(image):
    
    coordinates = []
    line_img_array=[]

    seg_mask = get_segmentation_mask(image)

    (H, W) = image.shape
    (newW, newH) = (512, 512)
    rW = W / float(newW)
    rH = H / float(newH)
    
    #Contour detection and bouding box generation.
    contours, hier = cv2.findContours(seg_mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        #cv2.rectangle(ori_img, (int(x*rW), int(y*rH)), (int((x+w)*rW),int((y+h)*rH)), (255,0,0), 1)
        coordinates.append((int(x*rW),int(y*rH),int((x+w)*rW),int((y+h)*rH)))
   
    #Cropping the lines from the original image using the bouding boxes generated above.
    for i in range(len(coordinates)-1,-1,-1):
        coors=coordinates[i]

        p_img=image[coors[1]:coors[3],coors[0]:coors[2]].copy()

        if p_img.shape[1] >= int(image.shape[1]/10):
            line_img_array.append(p_img)

        
    seg_image = cv2.drawContours(image, contours, -1, (0,255,0), 3)

    return line_img_array, seg_image
    


def get_segmentation_mask(image):
    
    original_shape = image.shape

    image = cv2.resize(image, (512,512))
    image = np.expand_dims(np.expand_dims(image, axis=0), axis=0)
    
    tensor_image = torch.from_numpy(image).float()

    seg_mask = model.forward(tensor_image).detach().numpy()    

    seg_mask = np.squeeze(np.squeeze(seg_mask, axis=0), axis=0)
    seg_mask = cv2.resize(seg_mask, (original_shape[1], original_shape[0]))

    seg_mask = cv2.normalize(src=seg_mask, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    cv2.threshold(seg_mask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU,seg_mask)

    return seg_mask


