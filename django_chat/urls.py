"""django_chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from chat_core import views
urlpatterns = [
    # Django管理页面
    url(r'^admin/?', admin.site.urls),



    # 获取更多message
    url(r'^room/moreMSG/?',views.moreMessage),

    # 新建聊天室
    url(r'^room/create/?',views.createRoom),

    # 获取聊天列表
    url(r'^room/getRooms/?', views.renderBack),

    # 进入聊天室
    url(r'^room/enter/?', views.enterRoom),

    # 登陆
    url(r'^user/login/?', views.doLogin),

    # 登出
    url(r'^user/logout/?',views.doLogout),

    # 注册用户
    url(r'^user/register/?',views.registerUser),

    # 获取用户详细信息
    url(r'^getUser/?',views.getUser),



    # 获取好友列表
    url(r'^user/friends/?',views.getFriends),

    # 添加好友
    url(r'^friend/add/?',views.addFriends),

    # 搜索用户
    url(r'^friend/search/?',views.searchFreind),

    # 删除好友
    url(r'^friend/delete/?',views.deleteFriend)

    # 修改备注

    # 获取好友信息


]

