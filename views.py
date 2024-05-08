from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import cv2
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import os
from playsound import playsound
import base64
from django.core.files.base import ContentFile

value = []

# Create your views here.
def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def basic(request):
    if request.method == 'GET':
       return render(request, 'basic.html', {})

def DetectEmotion(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        output = checkEmotion()
        context= {'data':output}
        return render(request, 'PlaySong.html', context)
    
def WebCam(request):
    if request.method == 'GET':
        data = str(request)
        formats, imgstr = data.split(';base64,')
        imgstr = imgstr[0:(len(imgstr)-2)]
        data = base64.b64decode(imgstr)
        with open('C:/Python/EmotionApp/static/photo/test.png', 'wb') as f:
            f.write(data)
        f.close()
        context= {'data':"done"}
        return HttpResponse("Image saved")
        

def Upload(request):
    if request.method == 'GET':
       return render(request, 'Upload.html', {})

def SongPlay(request):
    if request.method == 'POST':
      name = request.POST.get('t1', False)
      playsound('C:/Python/songs/'+name)
      output = '<center><font size=\"3\" color=\"white\">Your Mood Detected as : '+label+'<br/>Below are some selected songs based on your mood</font><br/></center><table align=\"right\">'
      output+='<tr><td><font size=\"3\" color=\"black\">Choose&nbsp;Song</td><td><select name=\"t1\">'
      for i in range(len(value)):
          output+='<option value='+value[i]+'>'+value[i]+'</option>'
          output+='</select></td></tr><tr><td></td><td><input type=\"submit\" value=\"Play\"></td></td></tr></table></body></html>'
      context= {'data':output}
      return render(request, 'PlaySong.html', context)  

def checkEmotion():
    detection_model_path = 'C:/Python/haarcascade_frontalface_default.xml'
    emotion_model_path = 'C:/Python/_mini_XCEPTION.106-0.65.hdf5'
    face_detection = cv2.CascadeClassifier(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    EMOTIONS = ["angry","disgust","scared", "happy", "sad", "surprised","neutral"]
    orig_frame = cv2.imread('C:/Python/EmotionApp/static/photo/test.png')
    orig_frame = cv2.resize(orig_frame, (48, 48))
    frame = cv2.imread('C:/Python/EmotionApp/static/photo/test.png',0)
    faces = face_detection.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
    print("==================="+str(len(faces)))   
    print(emotion_classifier)
    if len(faces) > 0:
        faces = sorted(faces, reverse=True,key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        roi = frame[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]
        path = 'C:/Python/songs'
        value.clear()
        for r, d, f in os.walk(path):
            for file in f:
                if file.find(label) != -1:
                    value.append(file)
        output = '<center><font size=\"3\" color=\"white\">Your Mood Detected as : '+label+'<br/>Below are some selected songs based on your mood</font><br/></center><table align=\"right\">'
        output+='<tr><td><font size=\"3\" color=\"black\">Choose&nbsp;Song</td><td><select name=\"t1\">'
        for i in range(len(value)):
            output+='<option value='+value[i]+'>'+value[i]+'</option>'
        output+='</select></td></tr><tr><td></td><td><input type=\"submit\" value=\"Play\"></td></td></tr></table></body></html>'
    else:
        output = '<font size=\"3\" color=\"black\">unable to predict emotion from image</font>'
    return output   
    
