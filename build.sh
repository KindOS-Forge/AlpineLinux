#!/bin/sh
set -eu

ALPINE_VERSION=3.18

# Check if the script is run as root.
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

PACKAGES=$(cat packages.txt | tr '\n' ' ')

# Build the project
echo "Building the project..."

rm -rf /tmp/build && mkdir -p /tmp/build && cd /tmp/build

wget https://raw.githubusercontent.com/alpinelinux/alpine-make-rootfs/v0.6.1/alpine-make-rootfs \
    && echo '73948b9ee3580d6d9dc277ec2d9449d941e32818  alpine-make-rootfs' | sha1sum -c \
    || exit 1

chmod +x alpine-make-rootfs

sudo ./alpine-make-rootfs \
    --branch ${ALPINE_VERSION} \
    --packages "${PACKAGES}" \
    --script-chroot \
    /tmp/example-$(date +%Y%m%d).tar.gz - <<'SHELL'
        # zero
SHELL