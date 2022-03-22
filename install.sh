git clone https://github.com/hasanramp/password-manager.git
sudo mv password-manager sife
cd sife
sudo pip3 install --editable .
sudo chmod 700 data/passwords.db
sudo chown root:root data/passwords.db
echo "It is recommended to install xclip."
echo "In ubuntu use: sudo apt instal xclip"
echo "In manjaro use: sudo pacman -S xclip"
echo "for other distributions, use the package manager to install xclip"
echo "type sife --help for information on how to use password-manager"
