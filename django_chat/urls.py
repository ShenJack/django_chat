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
    url(r'^admin/?', admin.site.urls),
    url(r'^room/?', views.enterRoom),
    url(r'^create/?',views.createRoom),
    url(r'^login/?', views.doLogin),
    url(r'^logout/?',views.doLogout),
    url(r'^register/?',views.registerUser),
    # url(r'^checkToken/?',views.checkToken),
    url(r'^getUser/?',views.getUser),
    url(r'^getRooms/?', views.renderBack),
]
