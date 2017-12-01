# -*- coding: UTF-8 -*-
from django.db import models
from django.utils import timezone
import base64


# Create your models here.


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)
    updateTime = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.label

    def as_dict(self):
        return {'name': self.name, 'label': self.label, 'update': self.updateTime.timestamp()}


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    receiver = models.TextField(default='')
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.timestamp.strftime("%H:%M")}


class Notification(models.Model):
    type= models.TextField()
    receiver = models.TextField()
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now())

    def as_dict(self):
        return {'type':self.type,'receiver':self.receiver,'content':self.content,'timestamp':self.timestamp}


class User(models.Model):
    username = models.TextField()
    nickName = models.TextField(default='')
    password = models.TextField()
    friends = models.ManyToManyField('self')
    createTime = models.DateTimeField(default=timezone.now())

    def as_dict(self):
        return {'nickname': self.nickName, 'name': self.username, 'createTime': self.createTime.timestamp()}
