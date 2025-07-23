from pathlib import Path

from transpire.resources import Deployment, Ingress, Secret, Service, PersistentVolumeClaim
from transpire.types import Image, ContainerRegistry
from transpire.utils import get_image_tag

name = "minecraft-server"
vanilla = "ocfmc-1-21-8"
gtnh = "gtnh"
auto_sync = True


def images():
    yield Image(name=vanilla, path=Path("/"), target=vanilla, registry=ContainerRegistry("ghcr"))
    yield Image(name=gtnh, path=Path("/"), target=gtnh, registry=ContainerRegistry("ghcr"))


def add_volumes(dep, name):
    dep.obj.spec.template.spec.volumes = [
        {"name": "data", "persistentVolumeClaim": {"claimName": name}},
    ]

    dep.obj.spec.template.spec.containers[0].volume_mounts = [
        {"name": "data", "mountPath": "/data"},
    ]


def objects():
    dep_vanilla = Deployment(
        name=vanilla,
        image=get_image_tag(vanilla),
        ports=[25565],
    )

    dep_vanilla.obj.spec.template.spec.dns_policy = "ClusterFirst"
    dep_vanilla.obj.spec.template.spec.dns_config = {"searches": ["ocf.berkeley.edu"]}

    add_volumes(dep_vanilla, vanilla)

    svc_vanilla = Service(
        name=vanilla,
        selector=dep_vanilla.get_selector(),
        port_on_pod=25565,
        port_on_svc=25565,
    )

    svc_vanilla_built = svc_vanilla.build()

    svc_vanilla_built["spec"]["type"] = "LoadBalancer"

    pvc_vanilla = PersistentVolumeClaim(
        name=vanilla,
        storage_class_name="rbd-nvme",
        access_modes=["ReadWriteOnce"],
        storage="32Gi"
    )

    yield dep_vanilla.build()
    yield svc_vanilla_built
    yield pvc_vanilla.build()

    dep_gtnh = Deployment(
        name=gtnh,
        image=get_image_tag(gtnh),
        ports=[25565],
    )

    dep_gtnh.obj.spec.template.spec.dns_policy = "ClusterFirst"
    dep_gtnh.obj.spec.template.spec.dns_config = {"searches": ["ocf.berkeley.edu"]}

    add_volumes(dep_gtnh, gtnh)

    svc_gtnh = Service(
        name=gtnh,
        selector=dep_gtnh.get_selector(),
        port_on_pod=25565,
        port_on_svc=25565,
    )

    svc_gtnh_built = svc_gtnh.build()

    svc_gtnh_built["spec"]["type"] = "LoadBalancer"

    pvc_gtnh = PersistentVolumeClaim(
        name=gtnh,
        storage_class_name="rbd-nvme",
        access_modes=["ReadWriteOnce"],
        storage="64Gi"
    )

    yield dep_gtnh.build()
    yield svc_gtnh_built
    yield pvc_gtnh.build()

