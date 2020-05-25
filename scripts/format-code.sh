docker build -t lifx-dev .
docker run -it lifx-dev yapf -vv -i -r -p --style pep8 .