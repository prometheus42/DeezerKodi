from .View import View

import os
import xbmc
import xbmcgui
import xbmcvfs
import xbmcplugin


class ChartView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(ChartView, self).__init__(scene, view_router, "chart", parent_view)
        self.lazy_chart = None

    def set_lazy_chart(self, lazy_chart):
        self.lazy_chart = lazy_chart

    def _get_lazy_chart(self):
        # try to get lazy chart from the parent if none are set
        if self.lazy_chart is None:
            self.lazy_chart = self.parent_view.get_lazy_chart()
        return self.lazy_chart

    # to display the albums
    def get_lazy_albums(self):
        chart = self._get_lazy_chart()()
        return lambda: self.scene.cache.get('chart_albums', default_producer=chart.get_albums)

    # to display the artists
    def get_lazy_artists(self):
        chart = self._get_lazy_chart()()
        return lambda: self.scene.cache.get('chart_artists', default_producer=chart.get_artists)

    # to display the playlists
    def get_lazy_playlists(self):
        chart = self._get_lazy_chart()()
        return lambda: self.scene.cache.get('chart_playlists', default_producer=chart.get_playlists)

    # to display the tracks
    def get_list_items(self):
        chart = self._get_lazy_chart()()
        list_items = []
        for track in self.scene.cache.get('chart_tracks', default_producer=chart.get_tracks):
            try:
                list_item = xbmcgui.ListItem(f"{track.artist.name} - {track.title}")
                list_item.setProperty('IsPlayable', 'true')
                list_item.setArt({'fanart': track.artist.picture_big, 'thumb': track.album.cover_big})
                self.add_item_track_info(list_item, track)
                list_items.append((self.get_url(f"/{track.id}"), list_item, False))
            except Exception as e:
                xbmc.log(str(e), xbmc.LOGERROR)
        return list_items

    # to diplay first menu
    def _show_chart_menu(self):
        items = {
            3005: {
                "image": xbmcvfs.translatePath(
                    os.path.join(self.scene.scene_router.images_path, "tracks-button.png")),
                "url": self.get_url('/tracks')
            },
            3006: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene.scene_router.images_path,
                                                         "myalbums-button.png")),
                "url": self.get_url('/albums')
            },
            3007: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene.scene_router.images_path,
                                                         "myartists-button.png")),
                "url": self.get_url('/artists')
            },
            3008: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene.scene_router.images_path,
                                                         "myplaylists-button.png")),
                "url": self.get_url('/playlists')
            }
        }
        list_items = []
        for key, item in items.items():
            list_item = xbmcgui.ListItem(self.scene.scene_router.language(key))
            list_item.setArt({'fanart': self.scene.scene_router.fanart_path, 'icon': item["image"]})
            list_items.append((item["url"], list_item, True))
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def show(self):
        self._show_chart_menu()
