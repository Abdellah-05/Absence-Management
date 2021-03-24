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
db = firebase.database()


class absence_student():
    def filieres(self):
        filieres=[]
        filiere=db.child("Filiers_Etudiants").get().val()
        for f in filiere:
            filieres.append(f)
        return filieres
    def add_student(self,f_name,l_name,f_n):
        name=str(l_name.upper()+"-"+f_name.capitalize())
        student=list(self.list_student(f_n))
        if name not in student:
            student.append(l_name.upper()+"-"+f_name.capitalize())
        db.child('Filiers_Etudiants').child(f_n).child('Etudiants').set(student)

    def edit_student(self,name,f_name,l_name,f_n):
        self.delete_student(name,f_n)
        self.add_student(f_name,l_name,f_n)

    def delete_student(self,name,f_n):
        student=list(self.list_student(f_n))
        student.remove(name)
        db.child('Filiers_Etudiants').child(f_n).child('Etudiants').set(student)

    def list_student(self,f_n):
        names=db.child("Filiers_Etudiants").child(f_n).get().val()['Etudiants']
        return names

    def dates_absence(self,f_n):
        dates_absences=[]
        dates=db.child('absence').child(f_n).get().val()
        for d in dates:
            dates_absences.append(d)
        return dates_absences

    def list_absence(self,f_n,dates):
        absence_global=[]
        for d in dates:
            c=db.child('absence').child(f_n).child(d).get().val()
        for n in (list(c.values())[0]):
            absence_global.append(n)
        return absence_global

    def absence_dictionary(self,f_n):
        list_students=[]
        list_absences=[]
        d={}
        list_students=self.list_student(f_n)
        dates=self.dates_absence(f_n)
        list_absences=self.list_absence(f_n,dates)
        for n in list_students:
            d[n]=list_absences.count(n)
        return d

#print(absence_student().absence_dictionary('IDSD-2'))
#absence_student().delete_student('DAMOU-Walid','IDSD-2')
#absence_student().add_student('walid','DAMOU','IDSD-2')

#db.child('Filiers_Etudiants').child('IDSD-2').child('Etudiants').set(["DAMOU-Walid","ELAAROUB-Abdellah","ATANANE-Othman","ELGARMAH-Ghizlane","BARABADE-Souad","QZIBRI-HIBA","HAOUD-Ayoub","HIMMID-Brahim","ELHANAFI-Yassine","ZAKARA-Salah_eddinne"])


class professor():
    
    def profs(self):
        profs=dict(db.child('Profs').get().val())
        return list(profs.keys())

    def add_professor(self,f_name,l_name,email,f_ensei):
        
        FilieresEnsiegnie = []
        for f in f_ensei :
            if f not in FilieresEnsiegnie:
                FilieresEnsiegnie.append(f.upper())

        p={"E-mail" : email,"FiliersEnseignes" : FilieresEnsiegnie,"Nom" : l_name.upper(),"Prenom" : f_name.capitalize()}
        prof=dict(db.child('Profs').get().val())
        name=l_name.upper()+'-'+f_name.capitalize()
        if name not in (list(prof.keys())):
            prof[name]=p
            db.child('Profs').set(prof)

    def delete_professor(self,name):
        profs=dict(db.child('Profs').get().val())
        del profs[name]
        db.child('Profs').set(profs)

    def edit_professor(self,f_name,l_name,email,f_ensei,prof_name):
        self.delete_professor(prof_name)
        self.add_professor(f_name,l_name,email,f_ensei)

#professor().add_professor('khadija','sadik','k.sadik@gmail.com',['IDSD-2','GI-1','ER-2'])
#professor().delete_professor('SADIK-Khadija')
#professor().profs()

class TimeTable():

    def dict_timetable(self,f_n):
        time_table=db.child('Filiers_Emploi').child(f_n).get().val()
        #print(dict(time_table)['Friday']['08-12'][0])
        return dict(time_table)

    def edit_timetable(self,f_n,day,hour,subject):
        time_table=TimeTable().dict_timetable(f_n)
        time_table[day][hour][0]=subject
        db.child('Filiers_Emploi').child(f_n).set(time_table)
        
    def delete_timetable(self,f_n):
        db.child('Filiers_Emploi').child(f_n).remove()

#TimeTable().timetable('IDSD-2')
#db.child('Filiers_Emploi').child("GE-2").child('Monday').set({'08-12':[' '],'14-18':[' ']})

class Admin():
    def getAdminInfo(self, mail):
        admins = db.child("Admins").get().val()
        adminInfo = {}
        for admin in admins:
            mailAdmin = db.child("Admins").child(admin).get().val()['E-mail']
            if mail == mailAdmin :
                adminInfo = {
                    "Prenom" : db.child("Admins").child(admin).get().val()['Prenom'],
                    "Nom" : db.child("Admins").child(admin).get().val()['Nom'],
                    "email" : db.child("Admins").child(admin).get().val()['E-mail']
                }
                return adminInfo
        return False

