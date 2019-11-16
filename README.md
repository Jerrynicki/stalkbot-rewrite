# Stalkbot Rewrite

A discord bot which lets your friends stalk you by using commands 

to activate your webcam, take (blurred) screenshots, play sounds,

play TTS messages and more.

### Cross-platform, although Windows support is still WIP

For a stable bot on Windows you can use [Meiyou's Stalkbot](https://github.com/M3IY0U/Stalkbot)

### To install (\*nix):
* Clone the repository `git clone https://gitlab.com/Jerrynicki/stalkbot-rewrite.git` or [download as zip](https://gitlab.com/Jerrynicki/stalkbot-rewrite/-/archive/master/stalkbot-rewrite-master.zip)
* Run the install.sh file in bash (`bash install.sh`). It will guide you through the installation

### To install (Windows):
* Clone the repository or [download as zip](https://gitlab.com/Jerrynicki/stalkbot-rewrite/-/archive/master/stalkbot-rewrite-master.zip)
* Download and install Python3 (>=3.6) from [python.org](https://python.org) (Make sure to select custom install and select tkinter and add it to your PATH!)
* Download an [ffmpeg binary](https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-4.2.1-win32-static.zip) and put the ffmpeg.exe in the same folder as the main.py
* Navigate to the folder you put the repository in and double-click the windows_installer.py file to guide you through the installation
* After installing you can double-click the main.py to start the bot

If you need help creating a bot account/getting a token, please refer to [this guide](https://discordpy.readthedocs.io/en/latest/discord.html)

### **In development!**

### To-Do:

* ~~Write documentation on how to set up the bot~~

* ~~Add feature for playing sound files~~

* Add feature for retrieving a list of processes with the must CPU/RAM usage

* Add feature for getting the current focused window

* Add feature for sending random files from specific folder

* ~~Add support for notifications~~

* ~~Add a GUI for editing the config, turning on/off specific features~~

* Add a command log and a user blacklist

Original bot with bad code at https://github.com/Jerrynicki/Stalkbot

*Licensed under the Modified BSD license. See the LICENSE.md file for more information.*
