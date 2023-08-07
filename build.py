#!/bin/python
import os
import sys



ALPINE_VERSION = "3.12.2"
ALPINE_ARCH = "x86_64"
ALPINE_MIRROR = "http://dl-cdn.alpinelinux.org/alpine"

short_version = ALPINE_VERSION.split(".")

downoad_url = f"{ALPINE_MIRROR}/v{ALPINE_VERSION}/releases/{ALPINE_ARCH}/alpine-minirootfs-{version}-{arch}.tar.gz"

curl -O https://dl-cdn.alpinelinux.org/alpine/v${ALPINE_VERSION}/releases/x86_64/alpine-minirootfs-${ALPINE_VERSION}${ALPINE_FIX}-x86_64.tar.gz
