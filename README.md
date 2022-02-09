
```
docker build --rm -t "name:latest" .
docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name name name
```
