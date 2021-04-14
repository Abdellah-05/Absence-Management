import socket
import pygame
from PIL import Image
import numpy as np
from cv2 import cv2
import face_recognition
import pickle
import time
from collections import Counter
import imutils

class Vidcamera1(object):
    def __init__(self):
        self.data11 = pickle.loads(open('encodings.pickle', "rb").read())
        self.inti = dict(Counter(self.data11["names"]))
        self.inti['Unknown'] = 1
        self.timer = 0
        self.previousImage = ""
        self.image = ""
        self.clock = pygame.time.Clock()
        self.video = cv2.VideoCapture(0)
        self.pr=''
    
    ## processing the frame.
    def process_frame(self,frame1):
        frame=frame1
        final_val=0
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.data11["encodings"], face_encoding)
            name = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = self.data11["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                final_val = counts[name]
            confidence_val = int((final_val/self.inti[name])*100)
            
            if confidence_val>90:
                face_names.append(name+':'+str(confidence_val))
                
            else:
                face_names.append('Unknown1_Unknown:'+str(confidence_val))
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX

            #-- traitement des nomes des étudiants
            if name.lower() == 'unknown':
                  Personne = 'Unknown ?'
            if name.lower() != 'unknown':
                  Prenom = name.split('_')[0][0] + '.'
                  firstName = name.split('_')[0]
                  print('--------------------> ', name)
                  if name.split(':')[0] == 'unknown':
                        name = "unknown_unknown:" + name.split(':')[1]
                  Nom = name.split('_')[1].split(':')[0]
                  Occ = name.split('_')[1].split(':')[1] + '%'
                  Personne = Prenom + Nom + ' ' + Occ
                  if Nom.lower() != 'unknown' :
                        self.pr = Nom + '-' + firstName                     
            cv2.putText(frame, Personne, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
            
            
        
        return frame

    #Main program loop:
    def framing(self):
          if self.timer < 1:
            success, data = self.video.read()
            frame = self.process_frame(data)
            
            self.timer = 0
          else:
            self.timer -= 1
          self.previousImage = self.image
          try:
            self.image = frame
          except:
            self.image = self.previousImage
          output = self.image
          self.clock.tick(1000)
          ret, jpeg = cv2.imencode('.jpg', output)
          return jpeg.tobytes(), self.pr
