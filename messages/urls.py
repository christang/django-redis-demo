from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from counts import views as count_views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/get/$', count_views.stats),
    url(r'^$', count_views.index),
)
