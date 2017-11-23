import time

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from chat_core.models import Room, User


class Alert:
    def __init__(self, room_id=None, alert=None, title=None, tip=None, tipUrl=None, ):
        self.alert = alert
        self.room_id = room_id
        self.title = title
        self.tip = tip
        self.tipUrl = tipUrl


def get_room(request):
    return render(request, )


def renderBack(request):
    rooms = reversed(Room.objects.order_by('updateTime')[:50])
    return render(request, 'home.html', {
        'logged': request.session['logged'],
        'username': request.session['username'],
        'title': "Home",
        'rooms': rooms
    })


def enterRoom(request):
    if not request.session['logged']:
        return redirect('/login/')
    if len(request.path.strip('/').split('/')) <= 1:
        data = request.POST
        try:
            room = Room.objects.get(name=data['room_id'])
        except Room.DoesNotExist:
            alert = Alert(data['room_id'], "%s Does Not Exist" % data['room_id'], "Does Not Exist", "试着创建一个？",
                          "/create/%s" % data['room_id'])
            return render(request, 'alert.html', {
                'logged': request.session['logged'],
                'username': request.session['username'],
                'alert': alert,
            })
        messages = reversed(room.messages.order_by('timestamp')[:50])
        return render(request, 'room.html', {
            'logged': request.session['logged'],
            'username': request.session['username'],
            'room': room,
            'messages': messages
        })
    else:
        prefix, room_id = request.path.strip('/').split('/')
        try:
            room = Room.objects.get(name=room_id)
        except Room.DoesNotExist:
            alert = Alert(room_id, "%s Does Not Exist" % room_id, "Does Not Exist", "试着创建一个？",
                          "/create/%s" % room_id)
            return render(request, 'alert.html', {
                'logged': request.session['logged'],
                'username': request.session['username'],
                'alert': alert,
            })
        messages = reversed(room.messages.order_by('timestamp')[:50])
        return render(request, 'room.html', {
            'logged': request.session['logged'],
            'username': request.session['username'],
            'room': room,
            'messages': messages
        })


def createRoom(request):
    post_data = request.POST
    try:
        room = Room.objects.get(label=post_data['room_id'])
    except Room.DoesNotExist:
        room = Room(label=post_data['room_id'], name=post_data['room_id'])
        room.save()
    # return redirect(request, 'room.html', {
    #     'room': room
    # },content_type='application/xhtml+xml')
    return HttpResponse('success')


def doLogin(request):
    if request.method == "GET":
        return render(request, 'login.html', {
            'logged': request.session['logged'],
            'username': request.session['username'],
        })
    elif request.method == "POST":
        data = request.POST
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            alert = Alert(alert='名字或者密码错误')
            return render(request, 'alert.html', {
                'alert': alert,
                'username': request.session['username'],
                'logged': request.session['logged']
            })

        if user.password != data['password']:
            alert = Alert(alert='名字或者密码错误')
            return render(request, 'alert.html', {
                'alert': alert,
                'username': request.session['username'],
                'logged': request.session['logged'],

            })
        else:
            request.session['username'] = username
            request.session['logged'] = True
            return redirect('/')


def doLogout(request):
    request.session['logged'] = False
    return redirect('/')


def generateKey(username, password):
    return str(time.time()) + username + password


def registerUser(request):
    if request.method == "GET":
        return render(request, 'register.html', {
            'logged': request.session['logged'],
            'username': request.session['username']
        })
    elif request.method == "POST":
        data = request.POST
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create(username=username, password=password)
            request.session['username'] = username
            request.session['logged'] = True
            return redirect('/')

        alert = Alert(alert=username + '已经存在')
        return render(request, 'alert.html', {
            'alert': alert,
            'logged': request.session['logged'],
            'username': request.session['username']
        })


def getUser(request):
    if request.session['username']:
        return HttpResponse(request.session['username'])
    else:
        return HttpResponse('nologin')
