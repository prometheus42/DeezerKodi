from .View import View

import xbmc
import xbmcgui
import xbmcplugin


class FlowView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(FlowView, self).__init__(scene, view_router, "flow", parent_view)
        self.lazy_tracks = None

    def set_lazy_tracks(self, lazy_tracks):
        self.lazy_tracks = lazy_tracks

    def _get_lazy_tracks(self):
        # try to get lazy tracks from the parent if none are set
        if self.lazy_tracks is None:
            self.lazy_tracks = self.parent_view.get_lazy_tracks()
        return self.lazy_tracks

    def get_list_items(self):
#        xbmc.log("FlowView - get ist items",level=xbmc.LOGNOTICE)
        list_items = []

        recentTracks = self._get_lazy_tracks()()
        for track in recentTracks:
            try:
                list_item = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title),
                                             thumbnailImage=track.album.cover_big)
                list_item.setProperty('IsPlayable', 'true')
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
                self.add_item_track_info(list_item, track)
                self.set_id(track.id)
                list_items.append((self.get_url("/%d" % track.id), list_item, False))
            except:
                pass
#        xbmc.log("FlowView - result: " + str(list_items),level=xbmc.LOGNOTICE)
        return list_items
