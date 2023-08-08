#!/bin/python3
import os
import sys
from tempfile import TemporaryDirectory
import urllib
import urllib.request
from pathlib import Path
from . import execute_command
from .container import Container


ALPINE_VERSION = "3.18.2"
ALPINE_ARCH = "x86_64"
ALPINE_MIRROR = "http://dl-cdn.alpinelinux.org/alpine"

os.environ['SOURCE_DATE_EPOCH'] = "1609459200"

short_version = '.'.join(ALPINE_VERSION.split(".")[:2])
download_url = f"{ALPINE_MIRROR}/v{short_version}/releases/{ALPINE_ARCH}/alpine-minirootfs-{ALPINE_VERSION}-{ALPINE_ARCH}.tar.gz"

container = Container(download_url)
container.run("sh")

cwd = os.getcwd()
cmd = f""" docker run \
    -v {cwd}/kindos-deploy:/kindos-deploy:ro \
    --name kindos \
    kindos \
    sh -c 'apk update && apk add python3 && /kindos-deploy/deploy.py'
"""
execute_command(cmd)
temp_file_name = Path(tmp.name) / "alpine.tar"
execute_command(f"docker export -o {temp_file_name} kindos")

# Reimport to docker to be ready for debug
execute_command(f"docker import {temp_file_name} kindos")
execute_command(f"gzip {temp_file_name} -c > {temp_file_name}.gz")

os.makedirs("dist", exist_ok=True)
execute_command(f"mv {temp_file_name}.gz dist/")
execute_command(f"sha256sum dist/kindos.tar.gz > dist/kindos.tar.gz.sha256")
with open("dist/kindos.tar.gz.sha256") as f:
    print(f.read())

size = os.path.getsize(f"dist/kindos.tar.gz")
print(f"Compressed size: {human_readable_size(size)}")