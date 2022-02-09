# Madesa
Run on Docker
```
docker build --rm -t "madesa:latest" .
docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name madesa madesa
```
