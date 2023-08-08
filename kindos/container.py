from dataclasses import dataclass
from . import execute_command

@dataclass
class Container:

    image_name: str = ""
    container_name: str = ""

    def _raw(self, cmd: str):
        cmd = f"docker {cmd}"
        return execute_command(cmd)

    def run(self, cmd: str="", bind_mounts: list=[]):
        name_cmd = f"--name {container_name}" if container_name else ""
        self._raw(f"run {self.image_name} {name_cmd} {cmd}")

    def exec(self: str, cmd: str):
        self._raw(f"exec {cmd}")

    def import_image(self, file_name: str):
        self._raw(f"import - {self.image_name} < {file_name}")