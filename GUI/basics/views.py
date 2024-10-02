from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages


def registerPage(request): 
    if request.method == 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        p1=request.POST.get('pass1')

        my_user=User.objects.create_user(uname,email,p1)
        my_user.save()
        return redirect('login')
    return render(request, 'register.html')
    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user) 
            return redirect('predict')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def result(request):
    return render(request,'prediction_result.html')

@login_required(login_url='login')
def quality(request):
    if(request.method=="POST"):
        data = request.POST 
        fixedacidity= float(data.get('textfixedacidity'))         
        volatileacidity=float(data.get('textvolatileacidity'))        
        citricacid=float(data.get('textcitricacid'))             
        residualsugar=float(data.get('textresidualsugar'))          
        chlorides=float(data.get('textchlorides'))               
        freesulfurdioxide=float(data.get('textfreesulfurdioxide'))     
        totalsulfurdioxide=float(data.get('texttotalsulfurdioxide'))    
        density=float(data.get('textdensity'))                 
        ph=float(data.get('textph'))                      
        sulphates=float(data.get('textsulphates'))               
        alcohol=float(data.get('textalcohol')) 
        if('inputsubmit' in request.POST):
            import pandas as pd
            path="C:/Users/Harsha C/Desktop/ML_Project/GUI/wine.csv"
            data=pd.read_csv(path)

            import sklearn
            from sklearn.preprocessing import LabelEncoder
            le_quality=LabelEncoder()

            data['quality_n']=le_quality.fit_transform(data['quality'])

            inputs=data.drop(['quality','quality_n'],axis=1)
            outputs=data['quality_n']

            import sklearn
            from sklearn.model_selection import train_test_split
            x_train,x_test,y_train,y_test=train_test_split(inputs,outputs,test_size=0.3)

            from sklearn.naive_bayes import GaussianNB
            model=GaussianNB()
            model.fit(x_train,y_train)
 
            y_pred=model.predict([[fixedacidity,volatileacidity,citricacid,residualsugar,chlorides,freesulfurdioxide,totalsulfurdioxide,density,ph,sulphates,alcohol]])
            # result=(y_pred)
            if y_pred==1: 
                result=("The provided wine details was tested and it is good quality ..!!! you can proceed")  
            else:
                result=("The provided wine details was tested and it has suspicious elements so it is a bad quality...!!! Do not proceed with that,it is harmfull")
                
            return render(request,'prediction_result.html',{'result':result})
        
    return render(request,'predict_quality.html')

    