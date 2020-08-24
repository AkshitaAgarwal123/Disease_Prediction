from django.shortcuts import render, redirect
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from .models import UserDb

usr = ""
sts = "Login"
def heart(request):
    """ 
    Reading the training data set. 
    """
    df = pd.read_csv('static/Heart_train.csv')
    data = df.values
    X = data[:, :-1]
    Y = data[:, -1:]

    """ 
    Reading data from the user. 
    """

    value = ''

    if request.method == 'POST':

        age = float(request.POST['age'])
        sex = float(request.POST['sex'])
        cp = float(request.POST['cp'])
        trestbps = float(request.POST['trestbps'])
        chol = float(request.POST['chol'])
        fbs = float(request.POST['fbs'])
        restecg = float(request.POST['restecg'])
        thalach = float(request.POST['thalach'])
        exang = float(request.POST['exang'])
        oldpeak = float(request.POST['oldpeak'])
        slope = float(request.POST['slope'])
        ca = float(request.POST['ca'])
        thal = float(request.POST['thal'])

        user_data = np.array(
            (age,
             sex,
             cp,
             trestbps,
             chol,
             fbs,
             restecg,
             thalach,
             exang,
             oldpeak,
             slope,
             ca,
             thal)
        ).reshape(1, 13)

        rf = RandomForestClassifier(
            n_estimators=16,
            criterion='entropy',
            max_depth=9
        )

        rf.fit(np.nan_to_num(X), Y)
        rf.score(np.nan_to_num(X), Y)
        predictions = rf.predict(user_data)

        if int(predictions[0]) == 1:
            value = 'have'
        elif int(predictions[0]) == 0:
            value = "don\'t have"
    global usr
    global sts

    return render(request,
                  'heart.html',
                  {
                      'context': value,
                      'usr': usr,
                      'sts': sts
                  })


def diabetes(request):
    """ 
    Reading the training data set. 
    """
    dfx = pd.read_csv('static/Diabetes_XTrain.csv')
    dfy = pd.read_csv('static/Diabetes_YTrain.csv')
    X = dfx.values
    Y = dfy.values
    Y = Y.reshape((-1,))

    """ 
    Reading data from user. 
    """
    value = ''
    if request.method == 'POST':

        pregnancies = float(request.POST['pregnancies'])
        glucose = float(request.POST['glucose'])
        bloodpressure = float(request.POST['bloodpressure'])
        skinthickness = float(request.POST['skinthickness'])
        bmi = float(request.POST['bmi'])
        insulin = float(request.POST['insulin'])
        pedigree = float(request.POST['pedigree'])
        age = float(request.POST['age'])

        user_data = np.array(
            (pregnancies,
             glucose,
             bloodpressure,
             skinthickness,
             bmi,
             insulin,
             pedigree,
             age)
        ).reshape(1, 8)

        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X, Y)

        predictions = knn.predict(user_data)

        if int(predictions[0]) == 1:
            value = 'have'
        elif int(predictions[0]) == 0:
            value = "don\'t have"
    global usr
    global sts
    return render(request,
                  'diabetes.html',
                  {
                      'context': value,
                      'usr': usr,
                      'sts': sts
                  })


def breast(request):
    """ 
    Reading training data set. 
    """
    df = pd.read_csv('static/Breast_train.csv')
    data = df.values
    X = data[:, :-1]
    Y = data[:, -1]
    print(X.shape, Y.shape)

    """ 
    Reading data from user. 
    """
    value = ''
    if request.method == 'POST':

        radius = float(request.POST['radius'])
        texture = float(request.POST['texture'])
        perimeter = float(request.POST['perimeter'])
        area = float(request.POST['area'])
        smoothness = float(request.POST['smoothness'])

        """ 
        Creating our training model. 
        """
        rf = RandomForestClassifier(
            n_estimators=16, criterion='entropy', max_depth=5)
        rf.fit(np.nan_to_num(X), Y)

        user_data = np.array(
            (radius,
             texture,
             perimeter,
             area,
             smoothness)
        ).reshape(1, 5)

        predictions = rf.predict(user_data)
        print(predictions)

        if int(predictions[0]) == 1:
            value = 'have'
        elif int(predictions[0]) == 0:
            value = "don\'t have"
    global usr
    global sts
    return render(request,
                  'breast.html',
                  {
                      'context': value,
                      'usr': usr,
                      'sts': sts
                  })


def handler404(request):
    return render(request, '404.html', status=404)




""" 
===========================================================================
Handling Authentication. 
===========================================================================
"""
def home(request):
    global usr, sts
    if request.method == 'POST':
        usr = str(request.POST.get('username', False))
        pwd = str(request.POST.get('password', False))

        f=0
        try:
            a = UserDb.objects.get(username=usr)
            if a.password != pwd:
                raise Exception
        except Exception:
            f=1
     
        if f==0:
            sts = "Logout"
            return render(request,
                        'home.html',
                        {
                          'usr': usr,
                          'sts': sts
                        })
        else:
            return redirect('/')
                        

def login(request):
    global usr, sts
    usr = ""
    sts = "Login"
    if request.method == 'POST':
        usr = "Invalid Credentials!"
    return render(request,
                'index.html',
                {
                    'usr': usr,
                    'sts': sts
                })



def signup(request):
    context=""
    if request.method == 'POST':
        myusername = str(request.POST['username'])
        myemail = str(request.POST['email'])
        mypassword = str(request.POST['password'])
        mydict = UserDb(username=myusername, email=myemail, password=mypassword)

        f = 0
        try:
            UserDb.objects.get(username=myusername)
        except Exception:
            print("New user added with username:"+myusername)
            f=1 
        if f==0:
            context = "Account Already Exsists, Enter Again!" 
        else:
            mydict.save()
            context = "Account Successfully Created, Login Now!"  

        return render(request,
                    'signup.html',
                    {
                        'context': context
                    })        

    elif request.method == 'GET':
        return render(request,
                    'signup.html',
                    {
                        'context': context
                    })
        
