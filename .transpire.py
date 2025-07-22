from pathlib import Path

from transpire.resources import Deployment, Ingress, Secret, Service
from transpire.types import Image, ContainerRegistry
from transpire.utils import get_image_tag

name = "minecraft-server"
auto_sync = True


def images():
    yield Image(name="ocfmc-1.21.8", path=Path("/"), registry=ContainerRegistry("ghcr"))


def add_volumes(dep):
    dep.obj.spec.template.spec.volumes = [
        {"name": "data", "persistentVolumeClaim": {"claimName": "ocfmc-1.21.8"}},
    ]

    dep.obj.spec.template.spec.containers[0].volume_mounts = [
        {"name": "data", "mountPath": "/data"},
    ]


def objects():
    dep = Deployment(
        name="ocfmc-1.21.8",
        image=get_image_tag(name),
        ports=[25565],
    )

    dep.obj.spec.template.spec.dns_policy = "ClusterFirst"
    dep.obj.spec.template.spec.dns_config = {"searches": ["ocf.berkeley.edu"]}

    add_volumes(dep)

    svc = Service(
        name="ocfmc-1.21.8",
        selector=dep.get_selector(),
        port_on_pod=25565,
        port_on_svc=25565,
    )

    ing = Ingress.from_svc(
        svc=svc,
        host="mc.ocf.berkeley.edu",
        path_prefix="/",
    )

    yield dep.build()
    yield svc.build()
    yield ing.build()
