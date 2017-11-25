import json
import time

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from chat_core.models import Room, User


# Create your views here.


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
    try:
        username = request.session['username']
    except KeyError:
        username = ""
    try:
        logged = request.session['logged']
    except KeyError:
        logged = False
    rooms = reversed(Room.objects.order_by('updateTime')[:50])
    return render(request, 'home.html', {
        'logged': logged,
        'username': username,
        'title': "Home",
        'rooms': rooms
    })


def enterRoom(request):
    try:
        username = request.session['username']
    except KeyError:
        username = ""
    try:
        logged = request.session['logged']
    except KeyError:
        logged = False

    try:
        if not request.session['logged']:
            return redirect('/login/')
    except KeyError:
        request.session['logged'] = False
        return redirect('/login/')
    if len(request.path.strip('/').split('/')) <= 1:
        data = request.POST
        try:
            room = Room.objects.get(name=data['room_id'])
        except Room.DoesNotExist:
            alert = Alert(data['room_id'], "%s Does Not Exist" % data['room_id'], "Does Not Exist", "试着创建一个？",
                          "/create/%s" % data['room_id'])
            return render(request, 'alert.html', {
                'logged': logged,
                'username': username,
                'alert': alert,
            })
        messages = reversed(room.messages.order_by('timestamp')[:50])
        return render(request, 'room.html', {
            'logged': logged,
            'username': username,
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
                'logged': logged,
                'username': username,
                'alert': alert,
            })
        messages = reversed(room.messages.order_by('timestamp')[:50])
        return render(request, 'room.html', {
            'logged': logged,
            'username': username,
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
    data = serializers.serialize("json",Room.objects.filter(label=post_data['room_id']))
    return JsonResponse(data=data,status=201,safe=False)


def doLogin(request):
    try:
        username = request.session['username']
    except KeyError:
        username = ""
    try:
        logged = request.session['logged']
    except KeyError:
        logged = False
    if request.method == "GET":
        return render(request, 'login.html', {
            'logged': logged,
            'username': username,
        })
    elif request.method == "POST":
        data = request.POST
        username = data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            alert = Alert(alert='名字或者密码错误')
            return render(request, 'alert.html', {
                'alert': alert,
                'username': username,
                'logged': logged
            })

        if user.password != data['password']:
            alert = Alert(alert='名字或者密码错误')
            return render(request, 'alert.html', {
                'alert': alert,
                'username': username,
                'logged': logged,

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
    try:
        username = request.session['username']
    except KeyError:
        username = ""
    try:
        logged = request.session['logged']
    except KeyError:
        logged = False
    if request.method == "GET":
        return render(request, 'register.html', {
            'logged': logged,
            'username': username
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
            return HttpResponse(status=201)

        alert = Alert(alert=username + '已经存在')
        return render(request, 'alert.html', {
            'alert': alert,
            'logged': logged,
            'username': username
        })


def getUser(request):
    try:
        username = request.session['username']
        return HttpResponse(request.session['username'])
    except KeyError:
        return HttpResponse('nologin')
