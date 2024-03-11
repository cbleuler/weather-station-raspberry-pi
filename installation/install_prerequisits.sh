#!/bin/sh

echo "Installing requirements..."
sudo apt install git python3-venv i2c-tools

echo "Installing docker..."
curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
sh /tmp/get-docker.sh

usermod -aG docker pi

echo "Installation completed. Logout and login to create docker containers..."