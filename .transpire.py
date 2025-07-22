from pathlib import Path

from transpire.resources import Deployment, Ingress, Secret, Service, PersistentVolumeClaim
from transpire.types import Image, ContainerRegistry
from transpire.utils import get_image_tag

name = "minecraft-server"
dep_name = "ocfmc-1-21-8"
auto_sync = True


def images():
    yield Image(name=dep_name, path=Path("/"), registry=ContainerRegistry("ghcr"))


def add_volumes(dep):
    dep.obj.spec.template.spec.volumes = [
        {"name": "data", "persistentVolumeClaim": {"claimName": dep_name}},
    ]

    dep.obj.spec.template.spec.containers[0].volume_mounts = [
        {"name": "data", "mountPath": "/data"},
    ]


def objects():
    dep = Deployment(
        name=dep_name,
        image=get_image_tag(dep_name),
        ports=[25565],
    )

    dep.obj.spec.template.spec.dns_policy = "ClusterFirst"
    dep.obj.spec.template.spec.dns_config = {"searches": ["ocf.berkeley.edu"]}

    add_volumes(dep)

    svc = Service(
        name=dep_name,
        selector=dep.get_selector(),
        port_on_pod=25565,
        port_on_svc=25565,
    )

    svc_built = svc.build()

    svc_built["status"] = { "loadBalancer": { "ingress": [{"ip": "169.229.226.85", "ipMode": "vip"}] } }

    pvc = PersistentVolumeClaim(
        name=dep_name,
        storage_class_name="rbd-nvme",
        access_modes=["ReadWriteOnce"],
        storage="32Gi"
    )

    yield dep.build()
    yield svc_built
    yield pvc.build()
