from .View import View

import os
import xbmc
import xbmcgui
import xbmcvfs
import xbmcplugin


class SearchView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(SearchView, self).__init__(scene, view_router, "search", parent_view)

    def _get_query(self):
        dialog = xbmcgui.Dialog()
        return dialog.input(self.scene.scene_router.language(self.id))

    def _search(self, query):
        # check if query is in the cache first
        if self.scene.cache.has('search_%s_%s' % (self.id, query)):
            return self.scene.cache.get('search_%s_%s' % (self.id, query))

        # otherwise do the search
        search = {
            3010: lambda q: self.scene.scene_router.api.search(query=q),
            3011: lambda q: self.scene.scene_router.api.search_artist(query=q),
            3012: lambda q: self.scene.scene_router.api.search_album(query=q),
            3013: lambda q: self.scene.scene_router.api.search_track(query=q)
        }
        if self.id in search:
            results = search[self.id](query)
            # and put the result in the cache
            self.scene.cache.set('search_%s_%s' % (self.id, query), results)
            return results
        return None

    def get_lazy_albums(self):
        # TODO: Make query local variable!
        self.query = ''
        # check if query isn't in the url already
        url_query = self.scene.scene_router.get_query().split("=")
        if "searchQuery" in url_query:
            self.query = url_query[1]
        else:
            self.query = self._get_query()
            self.scene.scene_router.set_query("searchQuery=%s" % self.query)

        if self.query != '':
            results = self._search(self.query)
            return lambda: results
        return lambda: []

    def get_lazy_artists(self):
        self.query = ''
        # check if query isn't in the url already
        url_query = self.scene.scene_router.get_query().split("=")
        if "searchQuery" in url_query:
            self.query = url_query[1]
        else:
            self.query = self._get_query()
            self.scene.scene_router.set_query("searchQuery=%s" % self.query)

        if self.query != '':
            results = self._search(self.query)
            return lambda: results
        return lambda: []

    def get_list_items(self):
        self.query = ''
        # check if query isn't in the url already
        url_query = self.scene.scene_router.get_query().split("=")
        if "searchQuery" in url_query:
            self.query = url_query[1]
        else:
            self.query = self._get_query()

        if self.query != '':
            results = self._search(self.query)

            list_items = []
            for track in results:
                try:
                    list_item = xbmcgui.ListItem(f"{track.artist.name} - {track.title}")
                    list_item.setProperty('IsPlayable', 'true')
                    list_item.setArt({'fanart': track.artist.picture_big, 'thumb': track.album.cover_big})
                    self.add_item_track_info(list_item, track)
                    list_items.append((self.get_url(f"/{track.id}?searchQuery={self.query}"), list_item, False))
                except Exception as e:
                    xbmc.log(str(e), xbmc.LOGERROR)
            return list_items
        return []

    # to display menu
    def _show_search_menu(self):
        items = {
            3010: {
                "image": xbmcvfs.translatePath(
                    os.path.join(self.scene.scene_router.images_path, "search-button.png")),
                "url": self.get_url('/3010/tracks')  # search all
            },
            3011: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene.scene_router.images_path,
                                                         "myartists-button.png")),
                "url": self.get_url('/3011/artists')  # search artist
            },
            3012: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene.scene_router.images_path,
                                                         "myalbums-button.png")),
                "url": self.get_url('/3012/albums')  # search album
            },
            3013: {
                "image": xbmcvfs.translatePath(
                    os.path.join(self.scene.scene_router.images_path, "search-button.png")),
                "url": self.get_url('/3013/tracks')  # search track
            }
        }
        list_items = []
        for key, item in items.items():
            list_item = xbmcgui.ListItem(self.scene.scene_router.language(key))
            list_item.setArt({'fanart': self.scene.scene_router.fanart_path, 'icon': item["image"]})
            list_items.append((item["url"], list_item, True))
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def show(self):
        self._show_search_menu()
