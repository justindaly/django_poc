from django.conf.urls import url, include
from conversate import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<partner_username>[\w-]+)/$', views.conversation),
    url(r'^send_message/(?P<partner_username>[\w-]+)/$', views.send_message),
    url(r'^api/', include(router.urls)),
    url(r'^api/(?P<partner_username>[\w-]+)/$', views.MessageList.as_view()),
    url(r'^api/(?P<partner_username>[\w-]+)/since/$', views.MessageSinceList.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
