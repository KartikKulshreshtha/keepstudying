from django.shortcuts import render, redirect, HttpResponse
from app.models import Room, Topic
from django.db.models import Q
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    
    # In this q, What ever the query of topics is passed will be stored like Python, Greedy.
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains=q)|
                                Q(description__icontains = q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'app/home.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        # With these two lines we gather the username and the password
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            # Here we are checking that the user exists in the database or not
            user = User.objects.get(username = username)
        except:
            # If not, we will show the flash message
            messages.error(request, 'User is not exists')
            
        # Here we are authenticating the user with the username and the password
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,  'Username/Password doesnot exists!!')
    context = {'page': page}
    return render(request, 'app/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('loginPage')
        else:
            messages.error(request, 'Some error ocurred during the registration process!!!')
    return render(request, 'app/login_register.html', {'form': form})

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'app/rooms.html', context)


@login_required(login_url='/loginPage')
def createroom(request):
    forms = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'forms': forms}
    return render(request, 'app/room_form.html', context)

@login_required(login_url='/loginPage')
def updateroom(request, pk):
    room = Room.objects.get(id = pk)
    # This line is to pre-filled the data into the form that will be edited
    forms = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")
    if request.method == "POST":
        # Here we are checking that which room to be update
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'forms': forms}
    return render(request, 'app/room_form.html', context)

@login_required(login_url='/loginPage')
def deleteRoom(request, pk):
    # This line is for which room is to be deleted
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    return render(request, 'app/delete_form.html', {'obj': room})