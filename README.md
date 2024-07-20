# Social Site Stop

This application monitors your web browser tabs and plays an alert sound when specified social media websites are detected in open tabs. The application starts automatically when your Mac boots up and runs continuously until manually stopped or the Mac is shut down.

##  Prerequisites

- Python 3.x
- `simpleaudio` Python library
- `osascript` for running AppleScripts on macOS

## Installation and Setup

### 1. Convert Sound File

Ensure your alert sound file is in `.wav` format. You can use `ffmpeg` to convert `.m4a` to `.wav`:

```sh
brew install ffmpeg
ffmpeg -i /Users/homesachin/Desktop/close.m4a /Users/homesachin/Desktop/close.wav


## Save the Python Script

Save the following script as social_site_stop.py on your desktop


## Create a LaunchAgent

Create a LaunchAgent property list file to run the script automatically at startup.


## Load the LaunchAgent

Load the LaunchAgent using launchctl

## Verify the LaunchAgent

Verify that the LaunchAgent is loaded and runnin


## Manually Start the Script

You can also manually start the script if needed

