import platform
import subprocess
import time
from threading import Event, Thread

import simpleaudio as sa

# Define the websites to check
websites = ["instagram.com", "facebook.com", "x.com"]

# Event to signal when to stop the sound
stop_event = Event()

# Function to check open tabs on different operating systems
def check_open_tabs():
    os_type = platform.system()
    open_tabs = []

    if os_type == "Windows":
        import pygetwindow as gw
        windows = gw.getAllTitles()
        open_tabs = [win for win in windows if any(site in win for site in websites)]

    elif os_type == "Darwin":  # macOS
        for browser in ["Safari", "Google Chrome", "Brave"]:
            try:
                if browser == "Safari":
                    script = '''
                    tell application "{0}"
                        set window_list to every window
                        repeat with the_window in window_list
                            set tab_list to every tab in the_window
                            repeat with the_tab in tab_list
                                set tab_url to URL of the_tab
                                if tab_url contains "{1}" or tab_url contains "{2}" then
                                    return true
                                end if
                            end repeat
                        end repeat
                        return false
                    end tell
                    '''.format(browser, websites[0], websites[1])
                elif browser == "Google Chrome" or browser == "Brave":
                    script = '''
                    tell application "{0}"
                        set window_list to every window
                        repeat with the_window in window_list
                            set tab_list to every tab in the_window
                            repeat with the_tab in tab_list
                                set tab_url to URL of the_tab
                                if tab_url contains "{1}" or tab_url contains "{2}" then
                                    return true
                                end if
                            end repeat
                        end repeat
                        return false
                    end tell
                    '''.format(browser, websites[0], websites[1])

                result = subprocess.check_output(['osascript', '-e', script])
                if result.strip() == b'true':
                    open_tabs.append(browser)
            except subprocess.CalledProcessError as e:
                print(f"AppleScript error for {browser}: {e}")
            except Exception as e:
                print(f"Unexpected error for {browser}: {e}")

    elif os_type == "Linux":
        try:
            result = subprocess.check_output(['wmctrl', '-l'])
            open_tabs = [line for line in result.decode().split('\n') if any(site in line for site in websites)]
        except subprocess.CalledProcessError as e:
            print(f"wmctrl error: {e}")
        except Exception as e:
            print(f"Unexpected error on Linux: {e}")

    return open_tabs

# Function to play sound
def play_alert_sound():
    sound_path = "/Users/homesachin/Desktop/close.wav"  # Update with the path to your sound file
    wave_obj = sa.WaveObject.from_wave_file(sound_path)
    stop_event.clear()
    play_thread = Thread(target=play_sound, args=(wave_obj,))
    play_thread.start()

    # Check every 5 seconds if the tabs are still open
    while not stop_event.is_set():
        open_tabs = check_open_tabs()
        if not open_tabs:
            stop_event.set()
        time.sleep(20)

def play_sound(wave_obj):
    play_obj = wave_obj.play()
    while not stop_event.is_set() and play_obj.is_playing():
        time.sleep(1)
    play_obj.stop()

# Main loop to check every 60 seconds
while True:
    try:
        open_tabs = check_open_tabs()
        if open_tabs:
            print(f"Detected websites in open tabs: {open_tabs}")
            play_alert_sound()
        else:
            print("No specified websites detected in open tabs.")
        time.sleep(60)
    except KeyboardInterrupt:
        print("\nProgram stopped manually.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(60)
