import json
import os

print("Welcome to the Stalkbot installer for Windows!\nLet's install some required pip packages first")

os.system("py -m pip install pygame discord.py Pillow gTTS win10toast requests opencv-python --user")

input("Press enter if the installation was successful.")

print("""Now to set up your bot config.
The options will be written to the file config.json. You can change them later.

All time values are in seconds.""")

# token cam_width cam_height webcam_delay screenshot_blur timeout prefix tts_voice max_message_length status notifications_format

token = input("Please input your bot token (you can get one by creating a bot account at https://discordapp.com/developers): ")
print("If you do not know your webcam width/height, just enter 0 for the following values and the default 320x240 will be used.")
cam_width = int(input("Please input the width of your webcam (px): "))
cam_height = int(input("Please input the height of your webcam (px): "))
webcam_delay = float(input("Please input the desired delay before taking a picture when the webcam command is used: "))
screenshot_blur = float(input("Please input the desired amount of blur when taking screenshots: "))
timeout = float(input("Please input the cooldown/timeout for commands: "))
prefix = input("Please input your desired bot prefix: ")
tts_voice = input("Please input the text-to-speech voice to use (Google TTS, e.g. 'en' for English, 'de' for German): ")
max_message_length = float(input("Please input the maximum length for tts/play commands: "))
status = input("Please input a status for the bot to be broadcasting (Playing xyz) (leave empty for none): ")

print("""


Specific strings in the notifications format will be replaced by values
COMMAND will be replaced by the command
AUTHOR will be replaced by the person who invoked the command
SERVER will be replaced by the server the command was invoked on
CHANNEL will be replaced by the channel the command was invoked in
An example format would be:
AUTHOR: COMMAND | SERVER CHANNEL
Which would produce the following output when Flexis sends a screenshot command in #bots on Supermarkt:
Flexis#1234: Screenshot | Supermarkt #bots""")

notifications_format = input("Please input the desired format for notifications: ")
folder = input("Please input a folder for the folder command: ")

config = {"token": token, "cam_width": cam_width, "cam_height": cam_height, "webcam_delay": webcam_delay, "screenshot_blur": screenshot_blur, "timeout": timeout, "prefix": prefix, "tts_voice": tts_voice, "max_message_length": max_message_length, "status": status, "notifications_format": notifications_format, "folder": folder}
json.dump(config, open("config.json", "w"))

print("Success! You can now run the bot.")
