git clone https://github.com/hasanramp/sife.git
cd sife
sudo pip3 install --editable .
sudo chmod 700 data/
sudo chown root:root data/
echo "It is recommended to install xclip."
echo "In ubuntu use: sudo apt instal xclip"
echo "In manjaro use: sudo pacman -S xclip"
echo "for other distributions, use the package manager to install xclip"
echo "type sife --help for information on how to use password-manager"
