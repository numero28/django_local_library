from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout

# Create your views here.
def index(request):
    message = "Hello, World"
    context = {'message': message}
    return render(request, 'users/index.html', context)

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('learning_logs/index.html')
            
            
    context = {'form' : form}
    return render(request, 'registration/register.html', context)
