#-*- coding: utf-8 -*-
import numpy as np
import cv2
from copy import deepcopy
import dlib
import math
import time
import sys
import json

PREDICTOR_PATH = "./shape_predictor_68_face_landmarks.dat"
cascade_path='./haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(cascade_path)
eye_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

def order_speaker():
    vidCap = cv2.VideoCapture('0.mp4')
    speakers_arr = []
    #Extracting the video information
    length = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT))
    width  = int(vidCap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidCap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = vidCap.get(cv2.CAP_PROP_FPS)
    
    seconds = int(round(length / fps))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    
    #Formatting the seconds into strings and adding a leading 0 in the case of 1 digit
    seconds = str(seconds)
    minutes = str(minutes)
    hours = str(hours)
    if len(seconds) == 1:
            seconds = "0" + seconds
    if len(minutes) == 1:
            minutes = "0" + minutes
    if len(hours) == 1:
            hours = "0" + hours
      
    landmark_points = {}
    agYuzOran_list = []
    agUzAcOran_list = []
    gozGenAcOran_list = []
    kasUzArOran_list = []
    burUzBurUstDudOran_list = []
    kasUzGozKasOran_list = []
    smile_count = 0
      
    #VideoData will be the data entry in the data base for the video. It is a json object
    #Depending on the implementation, multiple haars might be used. The haar entry in the object might be an array
    videoData = {"name" : "0.mp4" , "haar" : "haarcascade_frontalface_default.xml" , "frames" : str(length) , "height" : str(height) , "width" : str(width), "fps" : str(fps) , "length" : '%s:%s:%s' % (hours , minutes, seconds) }    
    
    winName = 'Facial Landmarks'
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winName,1600,1000)

    #To be able to index the faces, they need to be ordered.
    #The faces are ordered from left to right. In the case 2 faces are on the same X index, they are ordered top to bottom.
    o_f = []
    i=0
    ret,im = vidCap.read()
    while ret:
        i+=1
        print("Frame %d of %d" % ( i , length)) 
        
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
        #For loop over the ordered faces
        for (x,y,w,h) in o_f:
            try:
                #cv2.line(im,(x,y),(x+w,y),(255,255,0),1)
                #cv2.line(im,(x,y),(x,y+h),(255,255,0),1)
                #cv2.line(im,(x,y+h),(x+w,y+h),(255,255,0),1)
                #cv2.line(im,(x+w,y),(x+w,y+h),(255,255,0),1)
                #pos1 = ((x+w+10),(y))
                #cv2.putText(im, 'S : ' + str(speaker_counter), pos1,fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(0, 0, 255))
                
                
                #cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray= grayScale[y:y+h, x:x+w]
                roi_color = im[y:y+h, x:x+w]

                rect=dlib.rectangle(np.long(x),np.long(y),np.long(x+w),np.long(y+h))
                k=np.matrix([[p.x, p.y] for p in predictor(im, rect).parts()])


                for idx, point in enumerate(k):
                    landmark_points[idx] = (point[0, 0], point[0, 1])
                
                #Getting emotion for the face
                # nip length- face width ratio and nip length - nip width ratio ----------------------------------------------------------------------------------------------------------------------------
                aGenislik = math.sqrt(((landmark_points[54][0]-landmark_points[48][0])**2)+((landmark_points[54][1]-landmark_points[48][1])**2))
                yuzGenislik = math.sqrt(((landmark_points[12][0]-landmark_points[4][0])**2)+((landmark_points[12][1]-landmark_points[4][1])**2))

                agYuzOran = (yuzGenislik/aGenislik)

                agYuzOran_list.append(agYuzOran)

                agAciklik = math.sqrt(((landmark_points[57][0]-landmark_points[51][0])**2)+((landmark_points[57][1]-landmark_points[51][1])**2))

                agUzAcOran = (aGenislik/agAciklik)
                agUzAcOran_list.append(agUzAcOran)


                # Eye length-eye width rate --------------------------------------------------------------------------------------------------------------
                gozAcSol = math.sqrt(((landmark_points[40][0]-landmark_points[38][0])**2)+((landmark_points[40][1]-landmark_points[38][1])**2))
                gozGenSol = math.sqrt(((landmark_points[39][0]-landmark_points[36][0])**2)+((landmark_points[39][1]-landmark_points[36][1])**2))

                gozGenAcOran = (gozGenSol/gozAcSol)
                gozGenAcOran_list.append(gozGenAcOran)

                # eyebrow length ratio --------------------------------------------------------------------------------------------------------------------
                kasAralik = math.sqrt(((landmark_points[22][0]-landmark_points[21][0])**2)+((landmark_points[22][1]-landmark_points[21][1])**2))
                kasUzunluk = math.sqrt(((landmark_points[21][0]-landmark_points[17][0])**2)+((landmark_points[21][1]-landmark_points[17][1])**2))

                kasUzArOran = (kasUzunluk/kasAralik)
                kasUzArOran_list.append(kasUzArOran)

                # nose-upper lip rate ---------------------------------------------------------------------------------------------------
                burunUzunluk = math.sqrt(((landmark_points[30][0]-landmark_points[27][0])**2)+((landmark_points[30][1]-landmark_points[27][1])**2))
                burUstDudArasi = math.sqrt(((landmark_points[50][0]-landmark_points[33][0])**2)+((landmark_points[50][1]-landmark_points[33][1])**2))

                burUzBurUstDudOran = (burunUzunluk/burUstDudArasi)
                burUzBurUstDudOran_list.append(burUzBurUstDudOran)

                # upper part of eye-eyebrow rate ----------------------------------------------------------------------------------------------------------
                kasUzunluk = math.sqrt(((landmark_points[21][0]-landmark_points[17][0])**2)+((landmark_points[21][1]-landmark_points[17][1])**2))
                gozKasAralik = math.sqrt(((landmark_points[38][0]-landmark_points[20][0])**2)+((landmark_points[38][1]-landmark_points[20][1])**2))

                kasUzGozKasOran = (kasUzunluk/gozKasAralik)
                kasUzGozKasOran_list.append(kasUzGozKasOran)
                
                emotion = ""
                if(agYuzOran <= (2.15)):
                    if (agUzAcOran > 2.45):
                        emotion = 'Smiling'
                    else:
                        emotion = 'Laughing'
                else: # agYuzOran > 2.65
                    if(gozGenAcOran > 2.70):
                        if(kasUzGozKasOran > 3.20):
                            if (2.50 < kasUzArOran < 4.50):
                                pemotion = 'Angry'
                        else: # kasUzGozKasOran <= 3.15
                            emotion = 'Neutral'
                    else: # gozGenAcOran <= 2.70
                        if(kasUzGozKasOran <= 2.90):
                            if(agUzAcOran <= 2.20):
                                emotion = 'Shocked'
                            else: # agUzAcOran < 2.50
                                emotion = 'Scared'
                
                #Creating an entry for each face to place in the object
                speaker = {"speaker" : str(speaker_counter) , "x" : str(x) , "y" : str(y) , "width" : str(w) , "height" : str(h) , "frame" : str(i) , "emotion" : emotion }
                #Adding entry to array
                #print(speaker)
                speakers_arr.append(speaker)
                speaker_counter+=1
            except:
                print("Unexpected error:", sys.exc_info()[0])
        del o_f[:]
            
        ret,im = vidCap.read()
            
        #cv2.imshow(winName,im)
        if cv2.waitKey(10) & 0xff==ord('q'):
            break
            
            
    vidCap.release()
    cv2.destroyAllWindows()
    #At the end of the function, add the speaker array to the data array
    videoData["detected"] = speakers_arr
    json_str = json.dumps(videoData)   
    data_file = open("data.json", "w")
    data_file.write(json_str)
    data_file.close()
    
order_speaker()

    