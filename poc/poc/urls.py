from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'poc.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url(r'^conversate/', include('conversate.urls')),
]
