from pythreejs import (
    AmbientLight,
    BoxGeometry,
    Mesh,
    MeshLambertMaterial,
    PerspectiveCamera,
    Renderer,
    Scene
)


def create_room():

    cube = Mesh(
        geometry=BoxGeometry(2, 2, 2),
        material=MeshLambertMaterial(color="red")
    )

    camera = PerspectiveCamera(
        position=[5, 5, 5]
    )

    light = AmbientLight()

    scene = Scene(
        children=[cube, camera, light]
    )

    renderer = Renderer(
        scene=scene,
        camera=camera,
        width=800,
        height=600
    )

    return renderer