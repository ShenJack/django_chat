# API文档

## /room
**POST**

`urls`
```python
urlpatterns = [
    url(r'^admin/?', admin.site.urls),
    # room_id
    url(r'^room/?', views.enterRoom),
    # room_id
    url(r'^create/?',views.createRoom),
    #username,password
    url(r'^login/?', views.doLogin),
    # No Params
    url(r'^logout/?',views.doLogout),
    #username,password    
    url(r'^register/?',views.registerUser),
    #room_id return： id
    url(r'^getRooms/?', views.renderBack),
]
```



### Model
- Room
```python
class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)
    updateTime = models.DateTimeField(default=timezone.now)
```
- User
```python
class User(models.Model):
    username = models.TextField()
    password = models.TextField()
    createTime = models.DateTimeField(default=timezone.now())
```
- Message
```python
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
```