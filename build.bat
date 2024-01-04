@echo off
rem Run Docker-related commands
rem Note: Adjust the paths and commands as needed

rem Remove web-scraper container if it exists
docker container rm -f web-scraper 2>nul

rem Remove web-scraper image if it exists
docker image rm -f web-scraper 2>nul

rem Prune all unused builder data (automatic 'y' response)
echo y | docker builder prune -a

rem Build the web-scraper image
docker build --platform=linux/amd64 -t web-scraper .

rem Tag the image
docker tag web-scraper erikpi/web-scraper:host

rem Push the image to the Docker registry
docker push erikpi/web-scraper:host
