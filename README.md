# AutoCloud

## Introduction

**AutoCloud** is a Python script designed to start and interact with multiple online sessions of a free cloud computing service called OnWorks. Developed by Dr. Ankur, a doctor who codes for fun, this script aims to simplify and automate session management in OnWorks.

## Features

- Start multiple OnWorks sessions simultaneously.
- Interact with all sessions with same command.
- Easy to configure and extend.

## Files in the Repository

- `AutoCloud.py` - Main script to start OnWorks sessions.
- `CommandGenerator.py` - Script to generate key events command to put in commands.txt.
- `show_image.txt` - Contain session numbers separated by newline for which you want GUI image (Default=blank file).
- `close.txt` - If contain any character, AutoCloud will send close request to all sessions (Default=blank file).
- `commands.txt` - File containing keys or mouse events to be sent.
- `requirements.txt` - Dependencies.
- `unicode_keys.txt` - See below.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/dr-ankurcodes/AutoCloud.git
    cd AutoCloud
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
(Just run AutoCloud.py, it will start a session on onworks, for other configurations see below!!)

1. **Configuring Sessions:**
   - Modify the number of sessions to start by changing line 17 in `AutoCloud.py`:
     ```python
     sessions = 1
     ```
     Leave it if you want only 1 session.
     
   - If you want to start sessions from a specific number, modify line 18:
     ```python
     start_from = 1
     ```
     This line does nothing, it just modifies the session number to be started from, like if you modify it to 3, it will start the session/s from session no. 3. Leave it as it is in most cases.
     
2. **Generating GUI Images:**
   - To enable GUI images, set `gui` to 1 in line 20 of `AutoCloud.py`:
     ```python
     gui = 0  # Change to gui = 1
     ```
   - Specify the session numbers for which you want GUI images in `show_image.txt`, separated by new lines. Like if you have created 10 sessions starting from 1, then if you put 3 then 4 (after a newline) in this file, then only gui images for session number 3 and 4 will be generated, I have made this feature for nice resource management because it puts a load on cpu to update the gui each time the server updates it (that is the reason i haven't used pillow here)

3. **Setting Session Duration:**
   - Modify the duration for each session by changing line 39 in `AutoCloud.py`:
     ```python
     duration = 20 * 60  # Duration in seconds
     ```
     By Default Each session will last 20 mins, you can change this by modifying this line, generally each session will automatically close after 30 mins from server (I am not sure). Leave it as it is in most cases.

4. **Closing Sessions:**
   - Create a `close.txt` file with any character in it to send close requests to all sessions. Alternatively, you can simply close the script to quit.
   - I made this to officially send the close request to server, but you can simply close the script to quit and avoid this file.

5. **Handling Infinite Loop:**
   - The script runs in an infinite loop, closing all sessions after 20 minutes and restarting them after waiting for 100 seconds.
   - If a session fails to open (generally due to overcapacity on the OnWorks server), the script will try to restart it (up to 5 tries).

6. **Sending Commands (Important):**
   - Create your own `commands.txt` file with the keys or mouse events to be sent.
   - Example commands for keyboard:
     ```text
     3.key,2.39,1.1; #ascii key (39=')
     3.key,5.65293,1.1; #unicode key (65293=Enter)
     3.key,3.103,1.1; 3.key,3.103,1.0; # 1.1 = press key down, 1.0 = release key (1.1->1.0 will mean press) #ascii key (103=g)
     (Prefix 2. if key code < 100, 3. is for <1000, 4 is for < 10000, 5 is for >10000)
     ```
   - Example commands for mouse:
     ```text
     5.mouse,3.350,3.658,1.0; # Normal unclicked position (350x, 658y)
     5.mouse,3.350,3.658,1.1; # Left click
     (Prefix 2. if coordinate < 100, 3. is for <1000, 4 is for < 10000, 5 is for >10000)
     ```
   - The sample commands.txt I provided is for ctrl+alt+t then pressing enter, which is for opening terminal. As you can see there I have written pressing and releasing key event command without a space gap, then a space gap then another command and then there is a newline then another command (Enter), it's up to you to put a newline or not, but spaces are necessary otherwise there would be glitches in key pressing. Like this You should also put the pressing and releasing command without space and give next key command a space, each space is equivalent to 0.5 sec time.sleep() and each newline is equivalent to 1 sec time.sleep(). I have provided a unicode_keys.txt file which has some keys and their equivalent unicode number. For other keys you can use their equivalent ascii decimal number, for which i have provided a CommandGenerator.py (see below).

7. **Generating Key Events:**
   - Use `CommandGenerator.py` to generate key events for your commands.
   - I haven't implemented unicode keys in it yet, you have to manually add the equivalent command, if any, like for alt/enter/ctrl etc., for reference of unicode keys, see unicode_keys.txt.

## TODO

I don't know why, maybe due to resource leakage, this infinite loop pauses after 2-3 hours on laptop, but working nicely on android termux.

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).

**Additional Terms:**
- Commercial use of this code requires explicit permission from the author.
- Attribution to the author must be provided wherever the code is used.

## Contact

For any inquiries or support, please reach out to Dr. Ankur at [dr.ankurcodes@gmail.com](mailto:dr.ankurcodes@gmail.com).
