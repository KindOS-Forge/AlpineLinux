import re
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

from . import execute_command


@dataclass
class Container:
    image_name: str = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.rm()

    def download_image(self, url: str) -> str:
        # get suffix from url

        suffix = ".".join(Path(url).name.split(".")[1:])
        tmp_file = NamedTemporaryFile(suffix=suffix)
        """Download an image from an url and return the path to the downloaded image"""
        urllib.request.urlretrieve(url, tmp_file.name)
        return tmp_file.name

    def check_image(self):
        """if image is an url download it to a temporary location and return the path"""
        image_name = self.image_name
        if image_name.startswith("http"):
            if ".tar" not in self.image_name:
                raise Exception("Image must be a tar file")
            image_name = self.download_image(self.image_name)
        if ".tar" in image_name:
            image_name = self.import_image(self.image_name)
            self.image_name = image_name

    def run(self, cmd: str = "", name: str = "", bind_mounts: list = []):
        """Run a command inside a container"""

        # generate a name if not provided using uuid
        if not name:
            generated_uuid = uuid.uuid4()
            name = str(generated_uuid)[:8]
            self.container_name = name

        self.check_image()
        cmd = f"docker run --name {name} " + " ".join(
            [f"-v {mount}" for mount in bind_mounts] + [self.image_name, cmd]
        )
        execute_command(cmd)

    def import_image(self, image_name: str) -> str:
        """Import an image"""
        filename = image_name.split("/")[-1]
        tag_name = re.sub(r"\.tar\.gz$", "", filename)
        execute_command(f"docker import {image_name} {tag_name}")
        return tag_name

    def rm(self):
        """Remove the running container"""
        execute_command(f"docker rm {self.container_name} > /dev/null")

    def export(self, output_file: str):
        """Export the container to a tar file"""
        output_dir = Path(output_file).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        execute_command(f"docker export --output={output_file} {self.container_name}")
