#-*- coding: utf-8 -*-
import numpy as np
import cv2
from copy import deepcopy

cascade_path='./haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(cascade_path)


def order_speaker():
    vidCap = cv2.VideoCapture('0.mp4')

    winName = 'Facial Landmarks'
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winName,1600,1000)

    #ordered faces
    o_f = []
    i=0
    while True:

        i+=1
        ret,im = vidCap.read()
            
        grayScale = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        face = cascade.detectMultiScale(grayScale, 1.3, 10, 0|cv2.CASCADE_SCALE_IMAGE, minSize = (70,70))
        
        for c in range ( 0 , len(face)):
            o_f.append( [face[c][0] , face[c][1] , face[c][2] , face[c][3]] )
   
        #Sort multiple faces in the case there are multiple.
        if len(o_f) > 1:
            for x in range(0 , len(o_f) - 1):
                for y in range(x + 1 , len(o_f)):
                    if o_f[x][0] > o_f[y][0]:
                    #swap face
                        temp = deepcopy(o_f[x])
                        o_f[x] = deepcopy(o_f[y])
                        o_f[y] = deepcopy(temp)
                    elif o_f[x][0] == o_f[y][0]:
                    #x is equal, then check on y as well
                        if o_f[x][1] > o_f[y][1]:
                    #swap face
                            temp = deepcopy(o_f[x])
                            o_f[x] = deepcopy(o_f[y])
                            o_f[y] = deepcopy(temp)
            
        speaker_counter = 1
        for (x,y,w,h) in o_f:
            cv2.line(im,(x,y),(x+w,y),(255,255,0),1)
            cv2.line(im,(x,y),(x,y+h),(255,255,0),1)
            cv2.line(im,(x,y+h),(x+w,y+h),(255,255,0),1)
            cv2.line(im,(x+w,y),(x+w,y+h),(255,255,0),1)
            pos1 = ((x+w+10),(y))
            cv2.putText(im, 'S : ' + str(speaker_counter), pos1,fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(0, 0, 255))
            speaker_counter+=1
            
        del o_f[:]
            
        cv2.imshow(winName,im)
        if len(face) > 1:
            #Only save frames with more than one speaker
            cv2.imwrite("speakers/" + str(i) + ".jpg" , im)
        if cv2.waitKey(10) & 0xff==ord('q'):
            break

    vidCap.release()
    cv2.destroyAllWindows()
    
order_speaker()

