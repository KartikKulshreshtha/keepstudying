from django.shortcuts import render, HttpResponse

rooms = [
    {'id': 1, 'name': 'Lets learn Dynammic Programming'},
    {'id': 2, 'name': 'Lets learn Heap'},
    {'id': 3, 'name': 'Lets learn Recursion'},
    {'id': 4, 'name': 'Lets learn Backtracking'},
]

def home(request):
    context = {'rooms': rooms}
    return render(request, 'app/home.html', context)

def room(request, pk):
    return render(request, 'app/rooms.html')
