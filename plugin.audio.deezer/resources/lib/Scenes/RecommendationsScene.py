from .Scene import Scene
from ..cache import Cache
from .Views.ViewRouter import ViewRouter


class RecommendationsScene(Scene):
    def __init__(self, scene_router):
        super(RecommendationsScene, self).__init__(scene_router, "recommendations", "Recommendations Scene")

        self.cache = Cache("RecommendationsScene2")

        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self))
        view_router.root.set_lazy_recommendations(lambda: self.cache.get('recommendations', default_producer=self.scene_router.get_user().get_recommendations))
        self.set_view(view)

        self.cache.save()
