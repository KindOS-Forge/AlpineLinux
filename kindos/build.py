#!/bin/python3
import os
from .container import Container


ALPINE_VERSION = "3.18.2"
ALPINE_ARCH = "x86_64"
ALPINE_MIRROR = "http://dl-cdn.alpinelinux.org/alpine"

short_version = ".".join(ALPINE_VERSION.split(".")[:2])
download_url = f"{ALPINE_MIRROR}/v{short_version}/releases/{ALPINE_ARCH}/alpine-minirootfs-{ALPINE_VERSION}-{ALPINE_ARCH}.tar.gz"

container = Container(download_url)
container.run(
    "apk update ", #&& apk add python3 && /kindos-deploy/deploy.py",
    bind_mounts=[f"{os.getcwd()}/kindos-deploy:/kindos-deploy:ro"],
)
#container.export("dists/kindos.tar.gz")
