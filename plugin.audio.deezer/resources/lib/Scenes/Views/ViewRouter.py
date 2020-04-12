from .TracksView import TracksView
from .AlbumsView import AlbumsView
from .ArtistsView import ArtistsView, ArtistMenuView, ArtistTopView
from .PlaylistsView import PlaylistsView
from .RadioChannelsView import RadioChannelsView
from .ChartView import ChartView
from .SearchView import SearchView
from .RecentView import RecentView
from .FlowView import FlowView
from .RecommendationsView import RecommendationsView

import xbmc

class ViewRouter(object):
    def __init__(self, scene):
        self.scene = scene
        self.root = None

        self.views = {
            "tracks": lambda parent: TracksView(scene=self.scene, view_router=self, parent_view=parent),
            "albums": lambda parent: AlbumsView(scene=self.scene, view_router=self, parent_view=parent),
            "artists": lambda parent: ArtistsView(scene=self.scene, view_router=self, parent_view=parent),
            "playlists": lambda parent: PlaylistsView(scene=self.scene, view_router=self, parent_view=parent),
            "artistmenu": lambda parent: ArtistMenuView(scene=self.scene, view_router=self, parent_view=parent),
            "artisttop": lambda parent: ArtistTopView(scene=self.scene, view_router=self, parent_view=parent),
            "radiochannels": lambda parent: RadioChannelsView(scene=self.scene, view_router=self, parent_view=parent),
            "chart": lambda parent: ChartView(scene=self.scene, view_router=self, parent_view=parent),
            "search": lambda parent: SearchView(scene=self.scene, view_router=self, parent_view=parent),
            "recent": lambda parent: RecentView(scene=self.scene, view_router=self, parent_view=parent),
            "flow": lambda parent: FlowView(scene=self.scene, view_router=self, parent_view=parent),
            "recommendations": lambda parent: RecommendationsView(scene=self.scene, view_router=self, parent_view=parent)
        }

    # e.g path = /playlists/tracks/1234567
    # e.g path = /albums/123456/tracks
    def route(self, path):
        xbmc.log("ViewRouter - path: " + str(path),level=xbmc.LOGNOTICE)
        parts = path.split('/')
        parent = self.root
        id_last = None
        set_id = "false"

        for part in parts:
#            xbmc.log("ViewRouter - part: " + str(part),level=xbmc.LOGNOTICE)
            if part in self.views:
                if part.startswith('flow') or part.startswith('recent'):
                    #Special case for flow and recent as the id is before the final /tracks and not after
                    set_id = "true"
                view = self.views[part]
 #               xbmc.log("ViewRouter - view: " + str(view),level=xbmc.LOGNOTICE)
                parent = view(parent)
                if self.root is None:
                    self.root = parent
            else:
#              xbmc.log("ViewRouter - else",level=xbmc.LOGNOTICE)
                if parent is not None:
#                   xbmc.log("ViewRouter - set_id: " + str(part),level=xbmc.LOGNOTICE)
                    id_last = part
                    parent.set_id(part)
        if set_id.startswith('true') and id_last is not None:
            parent.set_id(id_last)
        return parent
