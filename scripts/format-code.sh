docker build -t lifx-dev .
docker run -v "$(pwd):/lifx/" -w /lifx/ -it lifx-dev yapf -vv -i -r -p --style pep8 .