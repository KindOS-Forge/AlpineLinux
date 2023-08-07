#!/bin/python3
import os
import sys
from tempfile import TemporaryDirectory
import urllib
import urllib.request
from pathlib import Path

ALPINE_VERSION = "3.18.2"
ALPINE_ARCH = "x86_64"
ALPINE_MIRROR = "http://dl-cdn.alpinelinux.org/alpine"

short_version = '.'.join(ALPINE_VERSION.split(".")[:2])
# GOOD: https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-minirootfs-3.18.2-x86_64.tar.gz
#  BAD: https://dl-cdn.alpinelinux.org/alpine/v3.18.2/releases/x86_64/alpine-minirootfs-3.18-x86_64.tar.gz
downoad_url = f"{ALPINE_MIRROR}/v{short_version}/releases/{ALPINE_ARCH}/alpine-minirootfs-{ALPINE_VERSION}-{ALPINE_ARCH}.tar.gz"

def human_readable_size(size: int) -> str:
    """ Returns human readable size """
    if size < 1024:
        return f"{size}B"
    size /= 1024
    if size < 1024:
        return f"{size:.2f}KB"
    size /= 1024
    if size < 1024:
        return f"{size:.2f}MB"
    size /= 1024
    return f"{size:.2f}GB"

def execute_command(cmd: str, ignore_errors: bool = False):
    """ Execute a command and raises exception if it fails """
    if os.system(cmd) != 0:
        if ignore_errors:
            return
        raise Exception(f"Failed to execute command:\n {cmd}")

tmp = TemporaryDirectory()
temp_file_name = Path(tmp.name) / "alpine.tar.gz"

# Download the file and write its content to the temporary file
with open(temp_file_name, "wb") as temp_file:
    try:
        with urllib.request.urlopen(downoad_url) as response:
                temp_file.write(response.read())
    except urllib.error.HTTPError as e:
        print(downoad_url, file=sys.stderr)
        raise Exception(f"Failed to download from {downoad_url}, error: {e}")


# Now you can use the content in the temporary file as needed
print(f"File downloaded and stored in: {temp_file_name}")
execute_command(f"docker import - kindos < {temp_file_name}")

execute_command(f"docker rm kindos", ignore_errors=True)


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

gzip_temp_file_name = Path(tmp.name) / "alpine.tar.gz"

# Use execute command to gzip the file because it is much faster than python gzip
#   ~= 4s with system gzip vs 8s with python gzip
execute_command(f"gzip {gzip_temp_file_name} --force")
execute_command(f"du -sh {gzip_temp_file_name}.gz")
size = os.path.getsize(f"{gzip_temp_file_name}.gz")
print(f"Compressed size: {human_readable_size(size)}")
os.makedirs("dist", exist_ok=True)
execute_command(f"mv {gzip_temp_file_name}.gz dist/kindos.tar.gz")