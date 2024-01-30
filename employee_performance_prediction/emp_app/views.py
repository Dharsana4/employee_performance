from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from sklearn.ensemble import RandomForestRegressor
from django.contrib import messages
# for call predict.html
def predict(request):
    return render(request, 'predict.html')
 
# for display result on same page
def result(request):
    data = pd.read_csv("C:\\Users\\HP\\Documents\\dps lab\\train_dataset.csv")
    data["wip"]=data["wip"].fillna(data["wip"].mean())
    X= data.iloc[:,:-1]
    y = data["actual_productivity"]
    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=42)
    
    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_regressor.fit(X_train, y_train)
    

    # Fitting the model
    
 
    val1 = float(request.GET['n1'])
    val2 = float(request.GET['n2'])
    val3 = float(request.GET['n3'])
    val4 = float(request.GET['n4'])
    val5 = float(request.GET['n5'])
     
    #  Predict the model
    
    pred = rf_regressor.predict([[val1, val2, val3, val4, val5]])
    result1 = ""
    if pred[0]<0.5:
        result1 = "Poor performance"
    else:
        result1 = "Good performance"
 
    return render(request, "predict.html", {"result2": result1})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("Received username:", username)
            print("Received password:", password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('predict')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
            print(form.errors)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def add_account_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']

            user = form.save(commit=False)
            user.password = password  # Storing password in plaintext
            user.save()
            login(request, user)
            return redirect('predict')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'add_account.html', {'form': form})
