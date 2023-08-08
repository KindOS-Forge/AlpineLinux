from .docker import Docker

docker = Docker("kindos", "kindos")
docker.run("")
docker.exec("sh")
