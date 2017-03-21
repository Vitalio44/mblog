from django.conf.urls import url

from simple.views import home, login

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/(\w*)', login, name='login')
]