from django.shortcuts import render, redirect
from app.models import Room, Topic
from django.db.models import Q
from .forms import RoomForm

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

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'app/rooms.html', context)


def createroom(request):
    forms = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'forms': forms}
    return render(request, 'app/room_form.html', context)


def updateroom(request, pk):
    room = Room.objects.get(id = pk)
    # This line is to pre-filled the data into the form that will be edited
    forms = RoomForm(instance=room)
    if request.method == "POST":
        # Here we are checking that which room to be update
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'forms': forms}
    return render(request, 'app/room_form.html', context)


def deleteRoom(request, pk):
    # This line is for which room is to be deleted
    room = Room.objects.get(id = pk)
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    return render(request, 'app/delete_form.html', {'obj': room})