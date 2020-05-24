docker build -t lifx-dev .
printf '\e[1;34m%-6s\e[m\n' "Running Typechecker"
docker run -it lifx-dev mypy lifx tests 
if [ $? != 0 ]
then
    exit 1
fi
printf '\e[1;34m%-6s\e[m\n' "Running Tests"
docker run -it lifx-dev pytest