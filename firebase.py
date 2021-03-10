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


#-- authentification
"""
auth = firebase.auth()
email = input('Email : ')
password = input('password : ')
if auth.sign_in_with_email_and_password(email,password) :
      print('valide')
else:
      print('no')
"""

"""
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
  "Nom" : "Guezzaz",
  "Prenom" : "Azidine",
  "FiliersEnseignes" : ["IDSD-2", "IDSD-1", "ISIL"],
  "E-mail" : "a.guezzaz@gmail.com"
}
db.child("Profs").child("Guezzaz-Azidine").set(Profs)


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