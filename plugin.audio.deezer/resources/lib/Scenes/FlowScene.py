from .Scene import Scene
from .Views.ViewRouter import ViewRouter

class FlowScene(Scene):
    def __init__(self, scene_router):
        super(FlowScene, self).__init__(scene_router, "flow", "Flow Scene")

        # we wont use cache for this scene, as it should reflect most recent state
        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self) + "/tracks")
        view_router.root.set_lazy_tracks(lambda: self.scene_router.get_user().get_flow())
        #view.set_lazy_tracks(lambda: self.scene_router.get_user().get_flow())
        self.set_view(view)