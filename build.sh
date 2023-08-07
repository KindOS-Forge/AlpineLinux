#!/bin/sh
set -eu

SCRIPT_DIR=$(cd $(dirname $0); pwd)

ALPINE_VERSION=3.18
ALPINE_FIX=.2

rm -rf /tmp/build && mkdir -p /tmp/build && cd /tmp/build

curl -O https://dl-cdn.alpinelinux.org/alpine/v${ALPINE_VERSION}/releases/x86_64/alpine-minirootfs-${ALPINE_VERSION}${ALPINE_FIX}-x86_64.tar.gz

# Import the image into docker
echo "Importing the image into docker..."
docker import - kindos-alpinelinux < alpine-minirootfs-${ALPINE_VERSION}${ALPINE_FIX}-x86_64.tar.gz
docker rm kindos || true
docker run -v ${SCRIPT_DIR}/kindos:/kindos \
    --name kindos \
    -it kindos-alpinelinux \
    sh -c "apk add python3 && python -m kindos"

docker export kindos > kindos-alpinelinux.tar
xz kindos-alpinelinux.tar
du -sh kindos-alpinelinux.tar.xz

