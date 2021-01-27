#!/bin/bash

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "Welcome to the Stalkbot installer!"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

read -p "Press Enter to continue." coolvariable

echo "First, please make sure the following packages are installed on your system and on your PATH: "
echo "scrot"
echo "notify-send / libnotify"
echo "pip3 / python3-pip"
echo "Tkinter for Python 3 / python3-tk"
echo "ffmpeg"
echo "libsdl1.2-dev"
echo "Please note that they may be named differently on your distribution"

read -p "Press Enter if you have made sure that these packages are installed.  " coolvariable

echo ""
echo "Installing required pip packages..."

pip3 install pygame psutil discord.py Pillow gTTS requests

echo ""
echo "Now to set up your bot config."
echo "The options will be written to the file config.json. You can change them later."
echo "Please read the explanation for every option carefully."
echo "All time values are in seconds."

read -p "Press Enter to continue." coolvariable

read -sp "Please input your bot token (you can get one by creating a bot account at https://discordapp.com/developers): " token
echo ""

echo "If you do not know your webcam width/height, just enter 0 for the following values and the default 320x240 will be used."
read -p "Please input the width of your webcam (px): " cam_width
read -p "Please input the height of your webcam (px): " cam_height

echo "Please input a smaller width and height of your webcam to be used for the webcam gif command,"
echo "since the images will be downscaled anyway (for a 3s gif the width will usually be around 400)"
echo "and most webcams support a higher framerate at lower resolutions"
echo "Like the normal width and height, you can set this to 0 and the bot will use a default of 320x240"
read -p "Smaller width (px): " small_cam_width
read -p "Smaller height (px): " small_cam_height

read -p "Please input the desired delay before taking a picture when the webcam command is used: " webcam_delay
read -p "Please input the desired length of a webcam gif (seconds): " gif_length
read -p "Please input the desired amount of blur when taking screenshots: " screenshot_blur
read -p "Please input the cooldown/timeout for commands: " timeout
read -p "Please input your desired bot prefix: " prefix
read -p "Please input the text-to-speech voice to use (Google TTS, e.g. 'en' for English, 'de' for German): " tts_voice
read -p "Please input the maximum length for tts/play commands: " max_message_length
read -p "Please input a status for the bot to be broadcasting (Playing xyz) (leave empty for none): " status

echo ""
echo ""
echo "Specific strings in the notifications format will be replaced by values"
echo "COMMAND will be replaced by the command"
echo "AUTHOR will be replaced by the person who invoked the command"
echo "SERVER will be replaced by the server the command was invoked on"
echo "CHANNEL will be replaced by the channel the command was invoked in"
echo "An example format would be:"
echo "AUTHOR: COMMAND | SERVER CHANNEL"
echo "Which would produce the following output when Flexis sends a screenshot command in #bots on Supermarkt:"
echo "Flexis#1234: Screenshot | Supermarkt #bots"

echo ""
read -p "Press Enter to continue." coolvariable

read -p "Please input the desired format for notifications: " notifications_format

read -p "Please input a folder for the folder command: " folder

echo "{\"token\": \"$token\", \"cam_width\": $cam_width, \"cam_height\": $cam_height, \"small_cam_width\": $small_cam_width, \"small_cam_height\": $small_cam_height, \"webcam_delay\": $webcam_delay, \"screenshot_blur\": $screenshot_blur, \"timeout\": $timeout, \"prefix\": \"$prefix\", \"tts_voice\": \"$tts_voice\", \"max_message_length\": $max_message_length, \"notifications_format\": \"$notifications_format\", \"status\": \"$status\", \"folder\": \"$folder\", \"gif_length\": $gif_length}" > config.json

echo "Config has been written."
echo ""
echo ""
echo "Thank you for using the Stalkbot installer! You can now start your bot by running python3 main.py"
read -p "Press Enter to exit." coolvariable
