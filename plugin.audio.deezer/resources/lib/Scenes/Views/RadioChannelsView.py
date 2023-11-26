from .View import View

import xbmc
import xbmcgui
import xbmcplugin


class RadioChannelsView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(RadioChannelsView, self).__init__(scene, view_router, "radiochannels", parent_view)
        self.lazy_radios = None

    def set_lazy_radios(self, lazy_radios):
        self.lazy_radios = lazy_radios

    def _get_lazy_radios(self):
        # try to get lazy radios from the parent if none are set
        if self.lazy_radios is None:
            self.lazy_radios = self.parent_view.get_lazy_radios()
        return self.lazy_radios

    def _show_radios(self):
        self.radios = self._get_lazy_radios()()
        list_items = []

        for i in range(0, len(self.radios)):
            try:
                radio = self.radios[i]
                list_item = xbmcgui.ListItem(radio.title)
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path, 'thumb': radio.picture_big})
                list_items.append((self.get_url("/%d/tracks" % i), list_item, True))
            except Exception as e:
                xbmc.log(str(e), xbmc.LOGERROR)
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def get_list_items(self):
        self.radios = self._get_lazy_radios()()
        radio = self.radios[self.id]

        list_items = []
        for track in radio.get_tracks():
            try:
                list_item = xbmcgui.ListItem(f"{track.artist.name} - {track.title}")
                list_item.setProperty('IsPlayable', 'true')
                list_item.setArt({'fanart': track.artist.picture_big, 'thumb': track.album.cover_big})
                self.add_item_track_info(list_item, track)
                list_items.append((self.get_url(f"/{track.id}"), list_item, False))
            except Exception as e:
                xbmc.log(str(e), xbmc.LOGERROR)
        return list_items

    def show(self):
        self._show_radios()
