import cv2
import sys as s
import numpy as np
scale=0.5
img=cv2.imread('Deepmind_2880x1620_Lede.jpg',0)
H = img.shape[0]
W = img.shape[1]
img = cv2.resize(img,(int(scale*W), int(scale*H)))
for i in range(np.shape(img)[0]):
    for j in range(np.shape(img)[1]):
#        #img[i,j][2]=img[i,j][2]+20
        img[i,j][0]=0
#        
#        if img[i,j][2]>150:
#            img[i,j][2]=0
cv2.imshow('ae',img)
cv2.imwrite('ae',img)
cv2.waitKey(0)
cv2.destroyAllwindows()