from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Room, Topic
from .forms import RoomForm

# Create your views here.


def home(request):
    # q = request.GET.get('q')
    # if q == None:
    #     rooms = Room.objects.all()
    # else:
    #     rooms = Room.objects.filter(topic__name__icontains=q)

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))

    topics = Topic.objects.all()
    room_count = rooms.count()

    return render(request, 'base/home.html', {'rooms': rooms, 'topics': topics, 'room_count': room_count})


def room(request, pk):
    room = Room.objects.get(id=pk)

    return render(request, 'base/room.html', {'room': room})


def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

    return render(request, 'base/room_form.html', {'form': form})


def updateRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()

            return redirect('home')

    return render(request, 'base/room_form.html', {'form': form})


def deleteRoom(request, pk):
    # room = Room.objects.get(id=pk)
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        room.delete()

        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})
