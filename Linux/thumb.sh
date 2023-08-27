apt-get update
sudo mkdir /home/swap && sudo fallocate -l 20GB /home/swap/swapfile && sudo chmod 600 /home/swap/swapfile && sudo mkswap /home/swap/swapfile && sudo swapon /home/swap/swapfile && echo '/home/swap/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
apt-get install -y fuse && sudo apt-get install -y fuse3
apt-get install -y screen
sudo apt install -y python3 && sudo apt install -y python3-pip
curl -k https://rclone.org/install.sh | sudo bash
apt install -y libgl1-mesa-glx