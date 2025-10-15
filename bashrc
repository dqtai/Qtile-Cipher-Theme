# If not running interactively, don't do anything 
[[ $- != *i* ]] && return 

stty -ixon # Disables ctrl-s and ctrl-q (Used To Pause Term)

shopt -s checkwinsize # Check the window size after each command and, if necessary, update the values of LINES and COLUMNS.

# Aliases
alias ..='cd ..' 
alias ...='cd ../..' 
alias gcf='cd $HOME/.config'
alias gdl='cd $HOME/Downloads'
alias search='nala search'
alias install='sudo nala install'
alias remove='sudo nala remove --purge'
alias update='sudo nala update'
alias upgrade='sudo nala upgrade'
alias uplist='apt list --upgradable'
# 
#
alias md='sudo mount UUID=37595265-2ca1-4ee0-8987-5f239fa30aed /home/user/Drive/'
alias pg='ping google.com'
alias fe='neofetch --kitty /home/user/.config/qtile/background.png --size 290px --color_blocks on'
#
# YT-DLP
alias yt='python3 ~/Documents/yt-dlp'
alias ytv='python3 ~/Documents/yt-dlp -S "height:1080" --merge-output-format mkv --embed-thumbnail --embed-metadata --embed-subs'
alias ytc='python3 ~/Documents/yt-dlp -S "height:1080" --merge-output-format mkv --embed-thumbnail --embed-metadata --embed-subs --download-archive channelName.txt'
alias yta='python3 ~/Documents/yt-dlp -f 'ba' -x --audio-format mp3'

# PS1 Customization
PS1='[\u@\h \W]\$ '

export PATH=~/.local/bin:$PATH

bash ~/Documents/year-progress.sh
