from django.conf.urls import url
from django.contrib import admin


from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    show_category,
    contacts,
    register,
    user_login,
    user_logout,
)

urlpatterns = [
    url(r'^$', post_list, name="list"),
    url(r'^create/$', post_create, name="create"),
    url(r'^contacts/$', contacts, name="contacts"),
    url(r'^registration/$', register, name="regist"),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$', post_detail, name="detail"),
    url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/up/$', post_update, name="update"),
    url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/del/$', post_delete, name="delete"),
    url(r'^(?P<slug>[-\w]+)/$', show_category, name='show_category'),

]

