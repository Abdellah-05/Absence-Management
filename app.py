## python -m http.server
## from the output folder to open http on 8000 port

from flask import Flask, render_template, request,Response, redirect, session
import os
from werkzeug.utils import secure_filename
import datetime
from own_pc import Vidcamera1


app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = r'C:\Users\gurvinder1.singh\Downloads\Facial-Similarity-with-Siamese-Networks-in-Pytorch-master\data\input_fold'
#app.config['OUTPUT_FOLDER'] = r'C:\Users\gurvinder1.singh\Downloads\Facial-Similarity-with-Siamese-Networks-in-Pytorch-master\data\output_fold'

import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCfhaX8-97PczmLPY5LxHdM8WyENToLov4",
    "authDomain": "absence-management-8e00e.firebaseapp.com",
    "databaseURL": "https://absence-management-8e00e-default-rtdb.firebaseio.com",
    "projectId": "absence-management-8e00e",
    "storageBucket": "absence-management-8e00e.appspot.com",
    "messagingSenderId": "266501909984",
    "appId": "1:266501909984:web:c0a3c895b7bc28449c0f85",
    "measurementId": "G-XE1KJ3PJLL"
  }

firebase = pyrebase.initialize_app(firebaseConfig)

DATE = datetime.datetime.now()
jour = DATE.strftime("%d")
mois = DATE.strftime("%m")
annee = DATE.year
heur = DATE.strftime("%H")
minutes = DATE.strftime("%M")
jourName = DATE.strftime("%A")

dateA = str(jour) + '-' + str(mois) + '-' + str(annee)
timeA = str(heur) + 'h' + str(minutes)
db = firebase.database()

#-- authentification

auth = firebase.auth()

@app.route('/', methods = ['GET'])
def loginGet():    
   return render_template('login.html')

@app.route('/', methods = ['POST'] )
def loginPost():
    email = request.form['email']
    password = request.form['password']
    #login_user(adminEmail)
    try:
        auth.sign_in_with_email_and_password(email,password)
        return redirect('/home')
    except:
        return render_template('login.html')

### front page 
@app.route('/home')
def front_page():
    return render_template('home.html')
   

## for own computer camera processing
@app.route('/video_1')
def index_1():
    return render_template('index.html')

def gen_1(camera):    
    absence = []
    while True:
        frame, vv = camera.framing()               
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        if vv not in absence and len(vv) > 6:        
            absence.append(vv)
 
     

@app.route('/video_feed_1')
def video_feed_1():
    print('video_feed method')
    aa=gen_1(Vidcamera1())
      
    print('video_feed method 2')
    
    return Response(aa,mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
   app.run(debug = True)
