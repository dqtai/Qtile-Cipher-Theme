#!/bin/bash

# Declare colors
red='\033[0;31m'
nc='\033[0m'
yellow='\033[0;33m'

# Directories
qtilevenv="$HOME/.local/src/qtile_venv"
bindir="$HOME/.local/bin"
qtileconfigdir="$HOME/.config/qtile"

# Either doas or sudo will work
[ -x "$(command -v doas)" ] && [ -e /etc/doas.conf ] && ld="doas"
[ -x "$(command -v sudo)" ] && ld="sudo"


$ld apt update -yy

$ld apt install xorg xserver-xorg python3 python3-pip python3-venv python3-v-sim python-dbus-dev \
    libpangocairo-1.0-0 python3-xcffib python3-cairocffi libxkbcommon-dev libxkbcommon-x11-dev \
    alsa-utils vim nemo kitty picom dunst libnotify-bin rofi neofetch -yy

# Installing Lightdm
sudo apt install lightdm -y
sudo systemctl enable lightdm

# Create folders in user directory (Documents, Downloads, etc.)
xdg-user-dirs-update

# Installing Qtile from source
[ -e "$qtilevenv" ] || python3 -m venv $qtilevenv 

[ -e "$bindir" ] || mkdir -p $bindir

git clone https://github.com/qtile/qtile.git $qtilevenv/qtile

$qtilevenv/bin/pip install $qtilevenv/qtile/. && echo "qtile start" >> $HOME/.xinitrc

if [ -e "$qtileconfigdir"/config.py ]; then 
	echo ""
	printf ${red}" NOTE:    ${yellow}using your existing config.py ${nc}\n"
	echo ""
else 
	mkdir $qtileconfigdir
	cp $qtilevenv/qtile/libqtile/resources/default_config.py $qtileconfigdir/config.py
	echo ""
	printf ${red}" NOTE:    ${yellow}copied default qtile config to $qtileconfigdir${nc}\n"
	echo ""
fi 

ln -sf $qtilevenv/bin/qtile $bindir && \
printf ${red}" NOTE:    ${yellow}QTILE binary is in $bindir ...\n \n ${red}Ensure $bindir is included in the PATH and REBOOT\n${nc} \n"

# Adding qtile.desktop to Lightdm xsessions directory
cat > ./temp << "EOF"
[Desktop Entry]
Name=Qtile
Comment=Qtile Session
Type=Application
Keywords=wm;tiling
EOF
sudo cp ./temp /usr/share/xsessions/qtile.desktop;rm ./temp
u=$USER
sudo echo "Exec=/home/$u/.local/bin/qtile start" | sudo tee -a /usr/share/xsessions/qtile.desktop


printf "\e[1;32mDone! you can now reboot.\e[0m\n"

