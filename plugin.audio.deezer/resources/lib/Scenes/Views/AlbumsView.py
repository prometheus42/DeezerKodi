from .View import View

import xbmcgui
import xbmc
import xbmcplugin


class AlbumsView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(AlbumsView, self).__init__(scene, view_router, "albums", parent_view)
        self.lazy_albums = None

    def set_lazy_albums(self, lazy_albums):
        self.lazy_albums = lazy_albums

    def _get_lazy_albums(self):
        # try to get lazy albums from the parent if none are set
        if self.lazy_albums is None:
            self.lazy_albums = self.parent_view.get_lazy_albums()
        return self.lazy_albums

    def _show_albums(self):
        self.albums = self._get_lazy_albums()()
        list_items = []

        for i in range(0, len(self.albums)):
            try:
                album = self.albums[i]
                list_item = xbmcgui.ListItem(album.title)
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path, 'thumb':album.cover_big})
                list_items.append((self.get_url("/%d/tracks" % i), list_item, True))
            except Exception as e:
                xbmc.log(str(e), xbmc.LOGERROR)
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def get_list_items(self):
        self.albums = self._get_lazy_albums()()
        album = self.albums[self.id]
        list_items = []

        for track in self.scene.cache.get('album_%s' % album.id, default_producer=album.get_tracks):
            try:
                list_item = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title))
                list_item.setProperty('IsPlayable', 'true')
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path, 'thumb':album.cover_big})
                self.add_item_track_info(list_item, track)
                list_items.append((self.get_url("/%d" % track.id), list_item, False))
            except Exception as e:
                xbmc.log(str(e), xbmc.LOGERROR)
        xbmc.log(str(list_items),level=xbmc.LOGINFO)
        return list_items

    def show(self):
        self._show_albums()
