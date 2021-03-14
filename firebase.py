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
  };

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
"""
#-- authentification

auth = firebase.auth()
email = input('Email : ')
password = input('password : ')
if auth.sign_in_with_email_and_password(email,password) :
      print('valide')
else:
      print('no')



#-- database
db = firebase.database()
Filiers_Emploi = {
  "Monday": {
    "08-12" : ["Machine Learning", "s.gounane@gmail.com"],
    "14-18" : ["Data Minig", "a.guezzaz@gmail.com"]
  },
  "Tuesday": {
    "08-12" : [],
    "14-18" : ["Data Minig", "a.guezzaz@gmail.com"]
  },
  "Wednesday": {
    "08-12" : [],
    "14-18" : []
  },
  "Thursday": {
    "08-12" : ["Machine Learning", "s.gounane@gmail.com"],
    "14-18" : ["Machine Learning", "s.gounane@gmail.com"]
  },
  "Friday": {
    "08-12" : [],
    "14-18" : []
  },
  "Saturday": {
    "08-12" : [],
    "14-18" : []
  }
    
}

db.child("Filiers_Emploi").child("IDSD-2").set(Filiers_Emploi)


Profs = {
  "Nom" : "GOUNANE",
  "Prenom" : "Said",
  "FiliersEnseignes" : ["IDSD-2", "IDSD-1", "ISIL"],
  "E-mail" : "s.gounane@gmail.com"
}
db.child("Profs").child("GOUNANE-Said").set(Profs)


Filiers_Etudiants = {
  "NomFilier" : "IDSD-2",
  "Etudiants" : ["ELAAROUB-Abdellah", "DAMOU-Walid", "ATNANE-Othmane"],
  "Presence": {
    "10-03-2021" : ["ELAAROUB-Abdellah", "DAMOU-Walid", "ATNANE-Othmane"]
  }
}
db.child("Filiers_Etudiants").child("IDSD-2").set(Filiers_Etudiants)



#-- Updte

#db.child("Filiers_Etudiants").child("IDSD-2").update({
#  "NomFilier" : 'IDSD-2'
#})

#Filiers_Etudiant = db.child("Filiers_Etudiants").child('IDSD-2').get()
#print('ok')
#print(Filiers_Etudiant.val())
#print(Filiers_Etudiant.key())

"""
import datetime
db = firebase.database()
DATE = datetime.datetime.now()

"""

absence = ["abdou", "walid"]

db.child("absence").child(dateA).child(timeA).set(absence)


prf = db.child("Profs").get()
for p in prf.each():
      print(p.val()["E-mail"])
      print(p.val()["FiliersEnseignes"])
      print(p.key())

jour = DATE.strftime("%d")
mois = DATE.strftime("%m")
annee = DATE.year
heur = DATE.strftime("%H")
minutes = DATE.strftime("%M")
jourName = DATE.strftime("%A")

dateA = jour + '-' + mois + '-' + str(annee)
timeA = heur + 'h' + minutes



     
      

def Seance(mail, jour, temps):
      
      filiersEmploi = db.child('Filiers_Emploi').get()
      for filier in filiersEmploi.each():
            try:  
              nomFilier = filier.key()              
              matiere, ensignantMail = filier.val()[jour][temps][0], filier.val()[jour][temps][1]
              if mail == ensignantMail :
                    return matiere, nomFilier 

            except:
              return False
      return False


if Seance('a.guezzaz@gmail.com', 'Monday', '14-18') != False :      
      a, b = Seance('a.guezzaz@gmail.com', 'Monday', '14-18')
      print(a)
      print(b)
else:
      print('ok')
"""
"""
def Seance(mail, jour, temps):
      
      filiersEmploi = db.child('Filiers_Emploi').get()
      prf = db.child("Profs").get()
      nomProf = ""
      tps = timeSeance.split('-')
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
"""
    
    #return render_template('home.html', matiereName = matiereName, filierName = filierName, ProfName = ProfName, SeanceTime = SeanceTime)

x='w'
def set():
  global x
  x='walid'

print(x)
set()
print(x)
