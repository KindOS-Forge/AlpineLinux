import urllib.request
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from . import execute_command
from pathlib import Path
import hashlib

@dataclass
class Container:
    image_name: str = ""

    def download_image(self, url: str) -> str:
        # get suffix from url

        suffix = '.'.join(Path(url).name.split(".")[1:])
        tmp_file = NamedTemporaryFile(suffix=suffix)
        """Download an image from an url and return the path to the downloaded image"""
        urllib.request.urlretrieve(url, tmp_file.name)
        return tmp_file.name

    def check_image(self):
        """ if image is an url download it to a temporary location and return the path """
        image_name = self.image_name
        if image_name.startswith("http"):
            if not '.tar' in self.image_name:
                raise Exception("Image must be a tar file")
            image_name = self.download_image(self.image_name)
        if '.tar' in image_name:
            image_name = self.import_image(self.image_name)
            self.image_name = image_name

    def run(self, cmd: str, bind_mounts: list = []):
        """Run a command inside a container"""
        self.check_image()
        cmd = "docker run " + " ".join(
            [f"-v {mount}" for mount in bind_mounts] + [self.image_name, cmd]
        )
        cmd += self.image_name
        execute_command(cmd)

    def import_image(self, image_name: str) -> str:
        """Import an image"""
        md5_hash = hashlib.md5(self.image_name.encode()).hexdigest()
        execute_command(f"docker import {image_name} {md5_hash}")
        return md5_hash