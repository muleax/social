#!/usr/bin/env bash

mkfs.ext4 /dev/nvme1n1
mount -t ext4 /dev/nvme1n1 /mnt/
echo "{ \"data-root\": \"/mnt/docker_ext/\" }" > /etc/docker/daemon.json

cd /mnt/
chown -R ec2-user .

sudo yum update -y
sudo yum install git -y
git clone https://github.com/muleax/social.git

sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo curl -L https://github.com/docker/compose/releases/download/1.25.0/docker-compose-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-compose > /dev/null
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

cd social
nohup docker-compose up --build > log.txt &
