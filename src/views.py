from multiprocessing import context
import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def register_view(request):
    form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

    context = {'form':form}
    return render(request, 'src/login_register.html', context)

def login_view(request):
    if request.user.is_authenticated == False:
        page = 'login'
        if request.method == 'POST':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or password invalid!')
    else:
        return redirect('home')

    context = {'page':page}
    return render(request, 'src/login_register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    if request.user.is_authenticated:
        task_list =  Task.objects.filter(user=request.user)
        context = {'task_list':task_list}
    else:
        context = {}
    return render(request, 'src/home.html', context)

@login_required(login_url='login')
def detail_view(request, pk):
    task = Task.objects.get(id=pk)
    context = {'task':task}
    return render(request, 'src/detail.html', context)

@login_required(login_url='login')
def create_view(request):
    form = TaskForm
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'src/task_form.html', context)

@login_required(login_url='login')
def delete_view(request, pk):
    task = Task.objects.get(id=pk)
    if task.user == request.user:      
        if request.method == 'POST':
            task.delete()
            return redirect('home')
        context = {'obj':task}
    else:
        return redirect('home')
    return render(request, 'src/delete.html', context)

@login_required(login_url='login')
def update_view(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if task.user == request.user:
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect('home')
    else:
        return redirect('home')
    context = {'form':form}
    return render(request, 'src/task_form.html', context)