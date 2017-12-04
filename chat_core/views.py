import json
import time

from django.core import serializers
from django.core.signals import request_finished
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
    # rooms = Room.objects.all()
    data = [room.as_dict() for room in rooms]

    return HttpResponse(status=200, content=json.dumps({
        'status': 'success',
        'data': data
    }))


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
            return HttpResponse(status=401, content=json.dumps({
                'error': '请登录后重试'
            }
            ))
    except KeyError:
        request.session['logged'] = False
        return HttpResponse(status=401, content=json.dumps({
            'error': '请登录后重试'
        }
        ))

    data = request.POST
    try:
        room = Room.objects.get(name=data['room_id'])
    except Room.DoesNotExist:
        return HttpResponse(status=404, content=json.dumps({
            'error': data['room_id'] + '不存在'
        }))
    messages = room.messages.order_by('timestamp')[:20]
    data = [i.as_dict() for i in messages]
    return HttpResponse(status=200, content=json.dumps({
        'room': room.as_dict(),
        'data': data
    }))


def createRoom(request):
    request_finished.connect(beforeLogin)
    post_data = request.POST
    try:
        room = Room.objects.get(label=post_data['room_id'])
    except Room.DoesNotExist:
        room = Room(label=post_data['room_id'], name=post_data['room_id'])
        room.save()
    # return redirect(request, 'room.html', {
    #     'room': room
    # },content_type='application/xhtml+xml')
    return JsonResponse(data=room.as_dict(), status=201, safe=False)


# 长连接开始 websocket链接成功
def doLogin(request):
    try:
        username = request.session['username']
    except KeyError:
        username = ""
    try:
        logged = request.session['logged']
    except KeyError:
        logged = False

    data = request.POST
    username = data['username']

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse(status=401, data={
            'error': '名字或者密码错误'
        })

    if user.password != data['password']:
        return JsonResponse(status=401, data={
            'error': '名字或者密码错误'
        })
    else:
        request.session['username'] = username
        request.session['logged'] = True
        return JsonResponse(status=200, data={
            'status': 'success',
            'data': user.as_dict()
        })


def doLogout(request):
    request.session['logged'] = False
    user = User.objects.get(username=request.session['username'])
    return JsonResponse(status=200, data={
        'status': 'success',
        'user': user.as_dict()
    })


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
            return HttpResponse(status=201, content=json.dumps(user.as_dict()))

        return JsonResponse(status=401, data={
            'error': 'already'
        })


def getUser(request):
    try:
        username = request.session['username']
        return HttpResponse(request.session['username'])
    except KeyError:
        return HttpResponse('nologin')


# GET MORE MESSAGE
def moreMessage(request):
    data = request.POST
    try:
        room = Room.objects.get(name=data['room_id'])
    except Room.DoesNotExist:

        return HttpResponse(status=404, content=json.dumps({
            'error': data['room_id'] + '不存在'
        }))
    messages = reversed(room.messages.order_by('timestamp'))
    # TODo


def getFriends(request):
    data = request.session
    username = data['username']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(status=403, content=json.dumps({
            'status': 'error',
            'error': '不存在'
        }))
    return HttpResponse(status=200, content={
        'status': 'success',
        'data': [i.as_dict() for i in user.friends.all()]
    })


# 添加好友
def addFriends(request):
    data = request.POST
    username = data['username']
    current_user = User.objects.get(username=request.session['username'])

    return None


# 搜索好友
def searchFreind(request):
    return None


def deleteFriend(request):
    return None


def beforeLogin(sender, **kwargs):
    print("Request finished!")
