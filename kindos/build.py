#!/bin/python3
import os

from .colors import INFO, OK, R
from .container import Container
from .size import human_readable_size

ALPINE_VERSION = "3.18"
ALPINE_FIX = ".3"
ALPINE_ARCH = "x86_64"
ALPINE_MIRROR = "http://dl-cdn.alpinelinux.org/alpine"

download_url = f"{ALPINE_MIRROR}/v{ALPINE_VERSION}/releases/{ALPINE_ARCH}/\
alpine-minirootfs-{ALPINE_VERSION}{ALPINE_FIX}-{ALPINE_ARCH}.tar.gz"

with Container(download_url) as container:
    container.run(
        "apk update ",  # && apk add python3 && /kindos-deploy/deploy.py",
        bind_mounts=[f"{os.getcwd()}/kindos-deploy:/kindos-deploy:ro"],
    )
    container.export("dist/kindos.tar.gz")

size = human_readable_size(os.path.getsize("dist/kindos.tar.gz"))
print(f"{OK} kindos.tar.gz: {INFO}{size}{R} byte(s)")
