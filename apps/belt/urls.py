from django.conf.urls import url
from . import views           
urlpatterns = [
url(r'^$',views.index),
url(r'^logval$',views.logval),
url(r'^regval$',views.regval),
url(r'^items$',views.show_items),
url(r'^wish_item/(?P<id>\d+)$',views.show),
url(r'^wish_items/create$',views.create),
url(r'^add_item$',views.add_item),
url(r'^remove/(?P<id>\d+)$',views.remove),
url(r'^add/(?P<id>\d+)$',views.add),
url(r'^logout$',views.logoutpage),
# url(r'^pokes/(?P<id>\d+)$',views.pokeUser),
]