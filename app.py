## python -m http.server
## from the output folder to open http on 8000 port

from flask import Flask, render_template, request,Response, redirect, session
import datetime
from own_pc import Vidcamera1
from management import absence_student , professor , TimeTable, Admin

app = Flask(__name__)
app.secret_key = 'ELAAROUB DAMOU'
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

print(jourName, minutes, heur)
dateA = str(jour) + '-' + str(mois) + '-' + str(annee)
timeA = str(heur) + 'h' + str(minutes)
db = firebase.database()

absence=[]
timeSeance = ""
presence = []
mailProf =""
matiereName = ""
filierName= ""
ProfName = ""

#------------------------------function_database---------------------------# 
def push_in_db(L,filiere, matiereName):
    global absence
    etudiants=db.child("Filiers_Etudiants").child(filiere).child("Etudiants").get().val()
    for e in etudiants:
        if e not in L:
            absence.append(e)
    db.child("absence").child(filiere).child(dateA).child(timeSeance).child(matiereName).set(absence)


#-- authentification

auth = firebase.auth()

@app.route('/', methods = ['GET'])
def loginGet():    
   return render_template('login.html')

@app.route('/', methods = ['POST'] )
def loginPost():
    global mailProf
    global timeSeance
    email = request.form['email']
    password = request.form['password']
    #login_user(adminEmail)
    try:
        auth.sign_in_with_email_and_password(email,password)
        mailProf = email
    
        if Admin().getAdminInfo(mailProf) != False :
            return redirect('/admin')
        if Admin().getAdminInfo(mailProf) == False :
            if int(heur) == 7 and int(minutes) >= 45 :
                timeSeance="08-12"
                return redirect('/home')
            if int(heur) == 13 and int(minutes) >= 45 :
                timeSeance="14-18"
                return redirect('/home')
            return redirect('/no_seance')
    except:
        return render_template('login.html')


def Seance(mail, jour, temps):
      filiersEmploi = db.child('Filiers_Emploi').get()
      prf = db.child("Profs").get()
      nomProf = ""
      tps = temps.split('-')
      SeanceTime = "De " + tps[0] + ":00 à " + tps[1] + ":00"
      for p in prf.each():
          if p.val()["E-mail"] == mail:
              nomProf = p.key()
      for filier in filiersEmploi.each():
            try:  
              nomFilier = filier.key()              
              matiere, ensignantMail = filier.val()[jour][temps][0], filier.val()[jour][temps][1]
              if mail == ensignantMail :
                    return matiere, nomFilier, nomProf, SeanceTime

            except:
              return False
      return False

### front page 
@app.route('/home')
def front_page():
    global filierName,matiereName
    if Seance(mailProf, jourName, timeSeance) == False :
        return redirect('/no_seance')
    
    matiereName, filierName, ProfName , SeanceTime = Seance(mailProf, jourName, timeSeance)
     
    return render_template('home.html', matiereName = matiereName, filierName = filierName, ProfName = ProfName, SeanceTime = SeanceTime)



@app.route('/no_seance')
def no_seance():
    prf = db.child("Profs").get()
    nomProf = ""
    
    for p in prf.each():
        if p.val()["E-mail"] == mailProf:
            nomProf = p.key()

    return render_template("no_seance.html" , Prof_name=nomProf)


### push in database 
@app.route('/done')
def push():
    push_in_db(presence,filierName,matiereName)
    return render_template('home.html')

## for own computer camera processing
@app.route('/video_1')
def index_1():
    return render_template('index.html')



def gen_1(camera):    
    while True:
        frame, vv = camera.framing()               
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        if vv not in presence and len(vv) > 6:        
            presence.append(vv) 
    #db.child("absence").child(dateA).child(timeA).set(absence) 

@app.route('/video_feed_1')
def video_feed_1():
    print('video_feed method')
    aa=gen_1(Vidcamera1())
      
    print('video_feed method 2')
    
    return Response(aa,mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/admin', methods = ['GET','POST'])
def admin():
    filieres=absence_student().filieres()
    profs=professor().profs()
    if request.method == "POST" :
        FName = request.form.get('FName')
        LName = request.form.get('LName')
        courses = request.form.get('courses')
        email = request.form.get('email')
        coursesList = courses.split(',')
        try:           
            professor().add_professor(FName, LName, email, coursesList)
        except:
            print("Warning to send data")
    return render_template('admin.html',filieres=filieres,profs=profs)


@app.route('/students', methods = ['GET','POST'])
def Students():
    Fname_list=[]
    Lname_list=[]
    filiere_n=request.form.get('searching_student')
    nombre_students=len(list(absence_student().list_student(filiere_n)))
    list_students=absence_student().list_student(filiere_n)
    for n in list_students:
        Fname_list.append(n.split('-')[1])
        Lname_list.append(n.split('-')[0])
    return render_template('students.html',filiere_n=filiere_n,nombre_students=nombre_students,list_students=sorted(list_students),Fname_list=Fname_list,Lname_list=Lname_list)

@app.route('/students/Add/<filiere_n>', methods = ['GET','POST'])
def AddStudents(filiere_n):
    first_name=request.form.get('FName')
    last_name=request.form.get('LName')
    try:
        absence_student().add_student(first_name , last_name , filiere_n)
    except:
        print('erreur')
    return redirect('/admin')

@app.route('/students/Edit/<filiere_n>/<name>', methods = ['GET','POST'])
def EditStudents(filiere_n,name):
    if request.method=='POST':
        print('post------------------')
        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
    try:
        absence_student().edit_student(str(name) , first_name , last_name , filiere_n)
    except:
        print('erreur in edit')
    return redirect('/admin')
    
@app.route('/students/delete/<filiere_n>/<name>', methods = ['GET','POST'])
def deleteStudents(filiere_n,name):
    absence_student().delete_student(name , filiere_n)
    return redirect("/admin")
@app.route('/prof', methods = ['GET','POST'])
def Prof():
    global prof_name
    prof_name=request.form.get('searching_prof')
    firstNameOf_Prof = prof_name.split('-')[0].lower()
    PrLastName = prof_name.split('-')[1]
    PrFirstName = prof_name.split('-')[0]
    email = db.child('Profs').child(prof_name).child('E-mail').get().val()
    filieres = db.child('Profs').child(prof_name).child('FiliersEnseignes').get().val()
    print(prof_name,  '-----------------------------------------------------')
    CSV_Filieres = filieres[0]
    for f in range(1, len(filieres)) :
        CSV_Filieres = CSV_Filieres + "," + filieres[f]        
    return render_template('prof.html',PrLastName=PrLastName, PrFirstName=PrFirstName, CSV_Filieres=CSV_Filieres, prof_name=prof_name,email=email,filieres=filieres, firstNameOf_Prof = firstNameOf_Prof)

@app.route('/time_table', methods = ['GET','POST'])
def time():
    global filiere_n
    filiere_n=request.form.get('searching_timetable')
    time_table=TimeTable().dict_timetable(filiere_n)
    return render_template('time_table.html',time_table=time_table,filiere_n=filiere_n)
      
    
@app.route('/save_time', methods = ['POST'])
def save_time():   
    #print(filiere_n) _table=TimeTable().dict_timetable(filiere_n)
    day=request.form.get('day')
    hour=request.form.get('hour')
    subject=request.form.get('subject')
    #print(day,hour,subject)
    TimeTable().edit_timetable(filiere_n,day,hour,subject)
    return redirect('/admin')

@app.route('/delete_time')
def delete_time():  
    TimeTable().delete_timetable(filiere_n)
    print("Done")
    return redirect('/admin')


@app.route('/edit_prof', methods = ['GET','POST'])
def EditProf():
    if request.method == "POST" :
        PrLastName = request.form.get('FName_')
        PrFirstName = request.form.get('LName_')
        filieres = request.form.get('courses_')
        print(filieres, "-----------------------------------------")
        email = request.form.get('email_')
        coursesList = filieres.split(',')
        print(PrFirstName)
        print(PrLastName)
        print(email)
        print(coursesList)
        try:          
            professor().edit_professor(PrFirstName, PrLastName, email, coursesList,prof_name)
        except:
            print("Warning to edit professor")
    return redirect('/admin')

@app.route('/prof/<nameProf>')
def DeleteProf(nameProf):
    print(nameProf, '---------------------')
    try :
        professor().delete_professor(nameProf)
    except:
        print('Warning in delete professor')
    return render_template('admin.html')

@app.route('/Absence/<prof_name>')
def Absence(prof_name):
    filiers=db.child('Profs').child(prof_name).child('FiliersEnseignes').get().val()
    print(filiers)
    return render_template('absence.html',filiers=filiers)

@app.route('/Absence/list/<filiere>')
def Absence_of_filiere(filiere):
    matiere=''
    for day in ['Monday' , 'Tuesday' , 'Wednesday' , 'Thursday' , 'Friday' , 'Saturday'] :
        for time in ['08-12' , '14-18'] :
            a=db.child('Filiers_Emploi').child(filiere).child(day).child(time).get().val()
            if a[1] == mailProf :
                matiere = a[0]
    list_student_hours=absence_student().absence_dictionary(filiere , matiere)
    return render_template('list_absence.html' , filiere=filiere , list_student_hours=list_student_hours)


if __name__ == '__main__':
   app.run(debug = True)