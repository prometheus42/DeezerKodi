from .Scene import Scene
import os
import xbmc
import xbmcvfs
import xbmcgui
import xbmcplugin


class MainScene(Scene):
    def __init__(self, scene_router):
        super(MainScene, self).__init__(scene_router, "main", "Main Scene")
        self._make_scene()

    def _make_scene(self):
        items = {
            2000: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene_router.images_path, "chart-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "chart")
            },
            2001: {
                "image": xbmcvfs.translatePath(
                    os.path.join(self.scene_router.images_path, "radiochannels-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "radiochannels")
            },
            2002: {
                "image": xbmcvfs.translatePath(
                    os.path.join(self.scene_router.images_path, "myplaylists-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "playlists")
            },
            2003: {
                "image": xbmcvfs.translatePath(
                    os.path.join(self.scene_router.images_path, "myalbums-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "albums")
            },
            2004: {
                "image": xbmcvfs.translatePath(
                    os.path.join(self.scene_router.images_path, "myartists-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "artists")
            },
            2005: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene_router.images_path, "search-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "search")
            },
            2006: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene_router.images_path, "recent-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "recent")
            },
            2007: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene_router.images_path, "flow-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "flow")
            },
            2008: {
                "image": xbmcvfs.translatePath(os.path.join(self.scene_router.images_path, "recommendations-button.png")),
                "url": "%s?scene=%s" % (self.scene_router.base_url, "recommendations")
            }
        }

        list_items = []

        for key, item in items.items():
            list_item = xbmcgui.ListItem(self.scene_router.language(key))
            list_item.setArt({'icon': item["image"], 'fanart': self.scene_router.fanart_path})
            list_items.append((item["url"], list_item, True))

        xbmcplugin.addDirectoryItems(self.scene_router.addon_handle, list_items)
