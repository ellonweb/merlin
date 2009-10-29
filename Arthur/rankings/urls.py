from django.conf.urls.defaults import *

urlpatterns = patterns('Arthur.rankings',
    url(r'^planets/$', 'planets.planets'),
    url(r'^planets/(?P<page>\d+)/$', 'planets.planets'),
    url(r'^planets/(?P<sort>\w+)/$', 'planets.planets'),
    url(r'^planets/(?P<sort>\w+)/(?P<page>\d+)/$', 'planets.planets'),
    url(r'^planets/(?P<race>\w+)/(?P<sort>\w+)/$', 'planets.planets'),
    url(r'^planets/(?P<race>\w+)/(?P<sort>\w+)/(?P<page>\d+)/$', 'planets.planets', name="planets"),
    url(r'^galaxy/(?P<x>\d+)[. :\-](?P<y>\d+)/$', 'galaxy.galaxy', name="galaxy"),
    url(r'^galaxies/$', 'galaxies.galaxies'),
    url(r'^galaxies/(?P<page>\d+)/$', 'galaxies.galaxies'),
    url(r'^galaxies/(?P<sort>\w+)/$', 'galaxies.galaxies'),
    url(r'^galaxies/(?P<sort>\w+)/(?P<page>\d+)/$', 'galaxies.galaxies', name="galaxies"),
)
