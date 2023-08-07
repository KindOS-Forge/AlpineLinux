#!/bin/python3
import os
import sys
from tempfile import NamedTemporaryFile


import tempfile
import urllib.request

ALPINE_VERSION = "3.18.2"
ALPINE_ARCH = "x86_64"
ALPINE_MIRROR = "http://dl-cdn.alpinelinux.org/alpine"

short_version = '.'.join(ALPINE_VERSION.split(".")[:2])
# GOOD: https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-minirootfs-3.18.2-x86_64.tar.gz
#  BAD: https://dl-cdn.alpinelinux.org/alpine/v3.18.2/releases/x86_64/alpine-minirootfs-3.18-x86_64.tar.gz
downoad_url = f"{ALPINE_MIRROR}/v{short_version}/releases/{ALPINE_ARCH}/alpine-minirootfs-{ALPINE_VERSION}-{ALPINE_ARCH}.tar.gz"


# Create a temporary file to store the downloaded content
with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    temp_file_name = temp_file.name

    # Download the file and write its content to the temporary file
    try:
        with urllib.request.urlopen(downoad_url) as response:
                temp_file.write(response.read())
    except urllib.error.HTTPError as e:
        print(downoad_url, file=sys.stderr)
        raise Exception(f"Failed to download from {downoad_url}, error: {e}")

    temp_file.flush()

# Now you can use the content in the temporary file as needed
print(f"File downloaded and stored in: {temp_file_name}")
os.system(f"docker import - kindos-alpinelinux < {temp_file_name}")


