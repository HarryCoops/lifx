docker build -t lifx-dev .
docker run -v "$(pwd):/lifx/" -w /lifx/ -it lifx-dev black lifx tests