## python -m http.server
## from the output folder to open http on 8000 port

from flask import Flask, render_template, request,Response
import os
from werkzeug.utils import secure_filename
#import recog
from own_pc import Vidcamera1



app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = r'C:\Users\gurvinder1.singh\Downloads\Facial-Similarity-with-Siamese-Networks-in-Pytorch-master\data\input_fold'
#app.config['OUTPUT_FOLDER'] = r'C:\Users\gurvinder1.singh\Downloads\Facial-Similarity-with-Siamese-Networks-in-Pytorch-master\data\output_fold'

### front page 
@app.route('/')
def front_page():
    
    return render_template('home.html')

## for own computer camera processing
@app.route('/video_1')
def index_1():
    return render_template('index.html')

def gen_1(camera):
    print('gen camera method')
    while True:
        frame = camera.framing()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    print('end of gen camera method')

    

    
    

@app.route('/video_feed_1')
def video_feed_1():
    print('video_feed method')
    aa=gen_1(Vidcamera1())
    
    
    print('video_feed method 2')
    
    return Response(aa,mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   app.run(debug = True)
