from .View import View

import os
import xbmc
import xbmcgui
import xbmcvfs
import xbmcplugin


class RecommendationsView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(RecommendationsView, self).__init__(scene, view_router, "recommendations", parent_view)
        self.lazy_recommendations = None

    def set_lazy_recommendations(self, lazy_recommendations):
        self.lazy_recommendations = lazy_recommendations

    def _get_lazy_recommendations(self):
        # try to get lazy recommendations from the parent if none are set
        if self.lazy_recommendations is None:
            self.lazy_recommendations = self.parent_view.get_lazy_recommendations()
        return self.lazy_recommendations

    # to display the albums
    def get_lazy_albums(self):
        recommendations = self._get_lazy_recommendations()()
        return lambda: self.scene.cache.get('recommendations_albums', default_producer=recommendations.get_albums)

    # to display the artists
    def get_lazy_artists(self):
        recommendations = self._get_lazy_recommendations()()
        return lambda: self.scene.cache.get('recommendations_artists', default_producer=recommendations.get_artists)

    # to display the playlists
    def get_lazy_playlists(self):
        recommendations = self._get_lazy_recommendations()()
        return lambda: self.scene.cache.get('recommendations_playlists', default_producer=recommendations.get_playlists)

    # to display the tracks
    def get_list_items(self):
        recommendations = self._get_lazy_recommendations()()
        list_items = []
        for track in self.scene.cache.get('recommendations_tracks', default_producer=recommendations.get_tracks):
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
    def _show_recommendations_menu(self):
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
        self._show_recommendations_menu()
