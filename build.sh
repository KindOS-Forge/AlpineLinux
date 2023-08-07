#!/bin/sh
set -eu

SCRIPT_DIR=$(cd $(dirname $0); pwd)

ALPINE_VERSION=3.18
ALPINE_FIX=.2

rm -rf /tmp/build && mkdir -p /tmp/build && cd /tmp/build

curl -O https://dl-cdn.alpinelinux.org/alpine/v${ALPINE_VERSION}/releases/x86_64/alpine-minirootfs-${ALPINE_VERSION}${ALPINE_FIX}-x86_64.tar.gz

# Import the image into docker
echo "Importing the image into docker..."
docker import - kindos < alpine-minirootfs-${ALPINE_VERSION}${ALPINE_FIX}-x86_64.tar.gz
docker run -v ${SCRIPT_DIR}/kindos:/kindos \
    --name kindos \
    kindos \
    sh -c "apk add --no-cache python3 && python -m kindos"

docker export kindos > kindos.tar
docker rm kindos
docker rmi kindos

echo "Compressing the image..."
gzip -9 kindos.tar
du -sh kindos.tar.gz

