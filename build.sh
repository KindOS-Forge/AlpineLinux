#!/bin/sh
set -eu

ALPINE_VERSION=3.18
ALPINE_FIX=.2

# # Check if the script is run as root.
# if [ "$(id -u)" -ne 0 ]; then
#     echo "Please run as root"
#     exit 1
# fi

rm -rf /tmp/build && mkdir -p /tmp/build && cd /tmp/build

curl -O https://dl-cdn.alpinelinux.org/alpine/v${ALPINE_VERSION}/releases/x86_64/alpine-minirootfs-${ALPINE_VERSION}${ALPINE_FIX}-x86_64.tar.gz

# Import the image into docker
echo "Importing the image into docker..."
docker import - kindos-alpinelinux < alpine-minirootfs-${ALPINE_VERSION}${ALPINE_FIX}-x86_64.tar.gz
docker run -v provision:/provision \
    -it kindos-alpinelinux sh

