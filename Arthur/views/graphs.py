# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2011 of Elliot Rosemarine.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import FuncFormatter
from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponse, HttpResponseNotFound
from Core.db import session
from Core.maps import Galaxy, GalaxyHistory, Planet, PlanetHistory, Alliance, AllianceHistory
from Arthur.loadable import loadable, load

urlpatterns = patterns('',
  url(r'^graphs/(?P<type>values|ranks)/', include(patterns('Arthur.views.graphs',
    url(r'^(?P<x>\d+)[. :\-](?P<y>\d+)[. :\-](?P<z>\d+)', 'planet', name="planetG"),
    url(r'^(?P<x>\d+)[. :\-](?P<y>\d+)', 'galaxy', name="galaxyG"),
    url(r'^(?P<name>[^/]+)', 'alliance', name="allianceG"),
  ))),
)

white   = '#ffffff'
black   = '#000000'
red     = '#ff0000'
green   = '#00ff00'
blue    = '#0000ff'
yellow  = '#ffff00'
magenta = '#ff00ff'
cyan    = '#00ffff'
pink    = '#ff6666'
bgcolor = '#292D3A'
axcolor = '#373B48'

class graphs(loadable):
    _num2short_scale = 1
    width = 500
    left, right = yellow, green
    
    plot = {'values' : lambda ax, Q: ((ax[1].plot(Q[0],Q[1],yellow),  "Size",),
                                      (ax[2].plot(Q[0],Q[2],green),   "Score",),
                                      (ax[2].plot(Q[0],Q[3],magenta), "Value",),
                                      ),
            'ranks' :  lambda ax, Q: ((ax[1].plot(Q[0],Q[1],yellow),  "Size",),
                                      (ax[2].plot(Q[0],Q[2],green),   "Score",),
                                      (ax[2].plot(Q[0],Q[3],magenta), "Value",),
                                      ),
            }
    
    def execute(self, request, user, type, x=None, y=None, z=None, name=None):
        width = self.width *(8.0/640)
        height = width *(6.0/8.0)
        fig = plt.figure(figsize=(width,height,), facecolor=bgcolor, edgecolor=bgcolor)
        try:
            ## Set up the axes
            fig.subplots_adjust(left=0.08,right=1-0.08,bottom=0.05,top=1-0.075)
            ax = {}
            
            ax[0] = fig.add_subplot(111)
            ax[0].yaxis.set_visible(False)
            ax[0].set_axis_bgcolor(axcolor)
            
            ax[1] = fig.add_axes(ax[0].get_position(True), sharex=ax[0], frameon=False)
            ax[1].yaxis.tick_left()
            ax[1].yaxis.set_label_position('left')
            ax[1].xaxis.set_visible(False)
            
            ax[2] = fig.add_axes(ax[0].get_position(True), sharex=ax[1], frameon=False)
            ax[2].yaxis.tick_right()
            ax[2].yaxis.set_label_position('right')
            ax[2].xaxis.set_visible(False)
            
            ## Load the data
            o = self.load(x,y,z,name)
            if not o:
                return self.error(fig,"Unable to load target x:%s y:%s z:%s name:%s"%(x,y,z,name,))
            
            q = self.query[type].filter_by(current=o)
            d = zip(*q.all())
            
            ## Plot the data and draw a legend
            leg = ax[0].legend(*zip(*self.plot[type](ax,d)), loc='upper left',
                                ncol=len(d)-1, columnspacing=1,
                                handlelength=0.1, handletextpad=0.5)
            leg.get_frame().set_facecolor(black)
            leg.get_frame().set_alpha(0.5)
            for t in leg.get_texts():
                t.set_color(white)
                t.set_fontsize(10)
            
            ## Sort out the axes
            ax[0].tick_params(labelcolor=white)
            
            ax[1].tick_params(labelcolor=self.left)
            ax[1].yaxis.set_major_formatter(FuncFormatter(lambda x,pos:self.num2short(x)))
            
            ax[2].tick_params(labelcolor=self.right)
            ax[2].yaxis.set_major_formatter(FuncFormatter(lambda x,pos:self.num2short(x)))
            
            if type == "ranks":
                # for ranks, invert axes, 0 at the top
                ax[0].set_ylim(top=0, bottom=ax[0].get_ylim()[1])
                ax[1].set_ylim(top=0, bottom=ax[1].get_ylim()[1])
                ax[2].set_ylim(top=0, bottom=ax[2].get_ylim()[1])
            else:
                # for values, scale all the way down to 0
                ax[0].set_ylim(bottom=0)
                ax[1].set_ylim(bottom=0)
                ax[2].set_ylim(bottom=0)
            
            ## Fix some odd behaviour
            ax[0].set_xlim(d[0][0], d[0][-1]) #align first tick to left
            ax[2].axvline(x=d[0][0], color=black) #fix gfx glitch on left yaxis
            
            ## Title
            title = self.title(o) + (" Rank" if type == "ranks" else "") + " History"
            fig.suptitle(title, color=white, fontsize=18)
            
            return self.render(fig)
        finally:
            plt.close(fig)
    
    def render(self, fig):
        canvas = FigureCanvas(fig)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response
    
    def error(self, fig, msg):
        fig.suptitle(msg, color=white)
        return HttpResponseNotFound(self.render(fig), content_type='image/png')

@load
class planet(graphs):
    load = staticmethod(lambda x, y, z, name: Planet.load(x,y,z))
    title = staticmethod(lambda o: "%s:%s:%s" %(o.x,o.y,o.z,))
    query = {'values' : session.query(PlanetHistory.tick, PlanetHistory.size, PlanetHistory.score, PlanetHistory.value),
             'ranks'  : session.query(PlanetHistory.tick, PlanetHistory.size_rank, PlanetHistory.score_rank, PlanetHistory.value_rank),
             }

@load
class galaxy(graphs):
    load = staticmethod(lambda x, y, z, name: Galaxy.load(x,y))
    title = staticmethod(lambda o: "%s:%s" %(o.x,o.y,))
    query = {'values' : session.query(GalaxyHistory.tick, GalaxyHistory.size, GalaxyHistory.score, GalaxyHistory.value),
             'ranks'  : session.query(GalaxyHistory.tick, GalaxyHistory.size_rank, GalaxyHistory.score_rank, GalaxyHistory.value_rank),
             }

@load
class alliance(graphs):
    load = staticmethod(lambda x, y, z, name: Alliance.load(name, exact=True))
    title = staticmethod(lambda o: "%s" %(o.name,))
    query = {'values' : session.query(AllianceHistory.tick, AllianceHistory.size, AllianceHistory.score, AllianceHistory.members),
             'ranks'  : session.query(AllianceHistory.tick, AllianceHistory.size_rank, AllianceHistory.score_rank, AllianceHistory.points_rank),
             }
    plot = {'values' : lambda ax, Q: ((ax[1].plot(Q[0],Q[1],yellow),  "Size",),
                                      (ax[2].plot(Q[0],Q[2],green),   "Score",),
                                      (ax[0].plot(Q[0],Q[3],pink),    "Members",),
                                      ),
            'ranks' :  lambda ax, Q: ((ax[1].plot(Q[0],Q[1],yellow),  "Size",),
                                      (ax[2].plot(Q[0],Q[2],green),   "Score",),
                                      (ax[0].plot(Q[0],Q[3],cyan),    "Points",),
                                      ),
            }
