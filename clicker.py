# v06

import time
import pyautogui
import argparse
import ast
import threading
import os
from datetime import datetime, timedelta

import mss
import cv2
import numpy as np


# -------- Timer --------
def show_timer(seconds, message=""):
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        print(f"{message}{mins:02d}:{secs:02d}", end="\r")
        time.sleep(1)
        seconds -= 1
    print()


def seconds_until_target(time_str):
    now = datetime.now()
    target = datetime.strptime(time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    if target <= now:
        target += timedelta(days=1)
    return int((target - now).total_seconds())


# -------- Recording --------
recording_flag = False
recorder_thread = None


def screen_recorder(output_file, fps=20):
    global recording_flag

    print("🎥 Recorder thread started")

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        width, height = monitor["width"], monitor["height"]

        print(f"Recording resolution: {width}x{height}")

        # Try MP4 first
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        # Fallback to AVI if MP4 fails
        if not out.isOpened():
            print("⚠️ MP4 failed, switching to AVI (XVID)...")
            output_file = output_file.replace(".mp4", ".avi")
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        if not out.isOpened():
            print("❌ ERROR: VideoWriter failed completely.")
            return

        print(f"📁 Saving to: {os.path.abspath(output_file)}")

        while recording_flag:
            img = sct.grab(monitor)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            out.write(frame)

        out.release()
        print(f"✅ Recording saved: {os.path.abspath(output_file)}")


def start_recording(output_dir):
    global recording_flag, recorder_thread

    recording_flag = True

    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(
        output_dir,
        f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    )

    recorder_thread = threading.Thread(
        target=screen_recorder,
        args=(filename,),
        daemon=False  # IMPORTANT
    )
    recorder_thread.start()


def stop_recording():
    global recording_flag, recorder_thread

    recording_flag = False

    if recorder_thread:
        recorder_thread.join()
        print("🛑 Recorder stopped cleanly")


# -------- Main Logic --------
def countdown(seconds, coordinates, delay_between=10, record=False, output_dir="."):
    print("Starting countdown...")
    show_timer(seconds, "Time left: ")

    print("\n⏰ Time's up!")

    if record:
        print("▶️ Starting screen recording...")
        start_recording(output_dir)
        time.sleep(1)  # give recorder time to initialize

    print("\n🖱️ Starting clicks...\n")

    for i, (x, y) in enumerate(coordinates):
        pyautogui.click(x, y)
        print(f"Clicked at ({x}, {y})")

        if i < len(coordinates) - 1:
            print(f"Waiting {delay_between} seconds...")
            show_timer(delay_between, "Next click in: ")

    if record:
        print("\n⏹️ Stopping recording...")
        stop_recording()


# -------- CLI --------
def main():
    parser = argparse.ArgumentParser(description="Auto clicker + screen recorder")

    parser.add_argument("--seconds", type=int)
    parser.add_argument("--time", type=str, help="HH:MM (24hr)")
    parser.add_argument("--coords", type=str, required=True)
    parser.add_argument("--delay", type=int, default=10)
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--output", type=str, default="recordings",
                        help="Directory to save recordings")

    args = parser.parse_args()

    if not args.seconds and not args.time:
        print("Provide --seconds or --time")
        return

    try:
        coordinates = ast.literal_eval(args.coords)
        if not isinstance(coordinates, list):
            raise ValueError
    except:
        print("Invalid coords format. Use: '[(x1,y1),(x2,y2)]'")
        return

    seconds = seconds_until_target(args.time) if args.time else args.seconds

    # macOS permission hint
    if args.record and os.uname().sysname == "Darwin":
        print("⚠️ Ensure Screen Recording permission is enabled for your terminal")

    countdown(seconds, coordinates, args.delay, args.record, args.output)


if __name__ == "__main__":
    main()


# v05 - record +  automate

# import time
# import pyautogui
# import argparse
# import ast
# import threading
# from datetime import datetime, timedelta

# import mss
# import cv2
# import numpy as np


# def show_timer(seconds, message=""):
#     while seconds >= 0:
#         mins, secs = divmod(seconds, 60)
#         timer = f'{mins:02d}:{secs:02d}'
#         print(f"{message}{timer}", end="\r")
#         time.sleep(1)
#         seconds -= 1
#     print()


# def seconds_until_target(time_str):
#     now = datetime.now()
#     target = datetime.strptime(time_str, "%H:%M").replace(
#         year=now.year, month=now.month, day=now.day
#     )

#     if target <= now:
#         target += timedelta(days=1)

#     return int((target - now).total_seconds())


# # -------- Screen Recording --------
# recording_flag = False

# def screen_recorder(output_file="recording.mp4", fps=20):
#     global recording_flag

#     with mss.mss() as sct:
#         monitor = sct.monitors[1]  # full screen

#         width = monitor["width"]
#         height = monitor["height"]

#         fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#         out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

#         while recording_flag:
#             img = sct.grab(monitor)
#             frame = np.array(img)

#             # Convert BGRA → BGR
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

#             out.write(frame)

#         out.release()
#         print(f"\nRecording saved to {output_file}")


# def start_recording():
#     global recording_flag
#     recording_flag = True

#     filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

#     thread = threading.Thread(target=screen_recorder, args=(filename,), daemon=True)
#     thread.start()

#     return thread


# def stop_recording():
#     global recording_flag
#     recording_flag = False


# # -------- Main Logic --------
# def countdown(seconds, coordinates, delay_between=10, record=False):
#     print("Starting countdown...")
#     show_timer(seconds, message="Time left: ")

#     print("Time's up!")

#     recorder_thread = None
#     if record:
#         print("Starting screen recording...")
#         recorder_thread = start_recording()

#     print("Starting clicks...\n")

#     for i, (x, y) in enumerate(coordinates):
#         pyautogui.click(x, y)
#         print(f"Clicked at ({x}, {y})")

#         if i < len(coordinates) - 1:
#             print(f"Waiting {delay_between} seconds before next click...")
#             show_timer(delay_between, message="Next click in: ")

#     if record:
#         print("Stopping recording...")
#         stop_recording()
#         time.sleep(2)  # give thread time to close


# def main():
#     parser = argparse.ArgumentParser(description="Countdown clicker with auto recording")

#     parser.add_argument("--seconds", type=int, help="Countdown time in seconds")
#     parser.add_argument("--time", type=str, help='Target time in HH:MM (24hr)')
#     parser.add_argument("--coords", type=str, required=True,
#                         help="List of coordinates, e.g. '[(100,200),(300,400)]'")
#     parser.add_argument("--delay", type=int, default=10)
#     parser.add_argument("--record", action="store_true", help="Enable screen recording")

#     args = parser.parse_args()

#     if not args.seconds and not args.time:
#         print("Provide either --seconds or --time")
#         return

#     try:
#         coordinates = ast.literal_eval(args.coords)
#         if not isinstance(coordinates, list):
#             raise ValueError
#     except:
#         print("Invalid coordinates format. Use: '[(x1,y1),(x2,y2)]'")
#         return

#     seconds = seconds_until_target(args.time) if args.time else args.seconds

#     countdown(seconds, coordinates, args.delay, args.record)


# if __name__ == "__main__":
#     main()


# v04 - record + manual

# import time
# import pyautogui
# import argparse
# import ast
# import subprocess
# import sys
# from datetime import datetime, timedelta


# def show_timer(seconds, message=""):
#     while seconds >= 0:
#         mins, secs = divmod(seconds, 60)
#         timer = f'{mins:02d}:{secs:02d}'
#         print(f"{message}{timer}", end="\r")
#         time.sleep(1)
#         seconds -= 1
#     print()


# def seconds_until_target(time_str):
#     now = datetime.now()
#     target = datetime.strptime(time_str, "%H:%M").replace(
#         year=now.year, month=now.month, day=now.day
#     )

#     if target <= now:
#         target += timedelta(days=1)

#     return int((target - now).total_seconds())


# def start_screen_recording():
#     print("Starting screen recording...")

#     if sys.platform == "darwin":  # macOS
#         # Uses QuickTime via AppleScript
#         subprocess.Popen([
#             "osascript",
#             "-e",
#             'tell application "QuickTime Player" to activate',
#             "-e",
#             'tell application "QuickTime Player" to new screen recording'
#         ])

#     elif sys.platform.startswith("linux"):
#         # Requires ffmpeg installed
#         subprocess.Popen([
#             "ffmpeg",
#             "-video_size", "1920x1080",
#             "-framerate", "25",
#             "-f", "x11grab",
#             "-i", ":0.0",
#             "output.mp4"
#         ])

#     elif sys.platform == "win32":
#         # Uses Xbox Game Bar (Win + Alt + R)
#         pyautogui.hotkey("win", "alt", "r")

#     else:
#         print("Screen recording not supported on this OS.")


# def countdown(seconds, coordinates, delay_between=10, record=False):
#     print("Starting countdown...")
#     show_timer(seconds, message="Time left: ")

#     print("Time's up!")

#     if record:
#         start_screen_recording()

#     print("Starting clicks...\n")

#     for i, (x, y) in enumerate(coordinates):
#         pyautogui.click(x, y)
#         print(f"Clicked at ({x}, {y})")

#         if i < len(coordinates) - 1:
#             print(f"Waiting {delay_between} seconds before next click...")
#             show_timer(delay_between, message="Next click in: ")


# def main():
#     parser = argparse.ArgumentParser(description="Countdown clicker script")

#     parser.add_argument("--seconds", type=int, help="Countdown time in seconds")
#     parser.add_argument("--time", type=str, help='Target time in HH:MM (24hr), e.g. "02:15"')
#     parser.add_argument("--coords", type=str, required=True,
#                         help="List of coordinates, e.g. '[(100,200),(300,400)]'")
#     parser.add_argument("--delay", type=int, default=10, help="Delay between clicks (seconds)")
#     parser.add_argument("--record", action="store_true", help="Start screen recording when timer ends")

#     args = parser.parse_args()

#     if not args.seconds and not args.time:
#         print("Provide either --seconds or --time")
#         return

#     try:
#         coordinates = ast.literal_eval(args.coords)
#         if not isinstance(coordinates, list):
#             raise ValueError
#     except:
#         print("Invalid coordinates format. Use: '[(x1,y1),(x2,y2)]'")
#         return

#     if args.time:
#         seconds = seconds_until_target(args.time)
#     else:
#         seconds = args.seconds

#     countdown(seconds, coordinates, args.delay, args.record)


# if __name__ == "__main__":
#     main()


# Usage:    python clicker.py --time 02:15 --coords "[(100,200),(300,400)]" --delay 10
# Usage:    python clicker.py --seconds 10 --coords "[(100,200),(300,400)]" --delay 10
# v03

# import time
# import pyautogui
# import argparse
# import ast
# from datetime import datetime, timedelta


# def show_timer(seconds, message=""):
#     while seconds >= 0:
#         mins, secs = divmod(seconds, 60)
#         timer = f'{mins:02d}:{secs:02d}'
#         print(f"{message}{timer}", end="\r")
#         time.sleep(1)
#         seconds -= 1
#     print()


# def seconds_until_target(time_str):
#     now = datetime.now()

#     # Parse HH:MM (24-hour format)
#     target = datetime.strptime(time_str, "%H:%M").replace(
#         year=now.year, month=now.month, day=now.day
#     )

#     # If already passed today → move to tomorrow
#     if target <= now:
#         target += timedelta(days=1)

#     return int((target - now).total_seconds())


# def countdown(seconds, coordinates, delay_between=10):
#     print("Starting countdown...")
#     show_timer(seconds, message="Time left: ")

#     print("Time's up! Starting clicks...\n")

#     for i, (x, y) in enumerate(coordinates):
#         pyautogui.click(x, y)
#         print(f"Clicked at ({x}, {y})")

#         if i < len(coordinates) - 1:
#             print(f"Waiting {delay_between} seconds before next click...")
#             show_timer(delay_between, message="Next click in: ")


# def main():
#     parser = argparse.ArgumentParser(description="Countdown clicker script")

#     parser.add_argument("--seconds", type=int, help="Countdown time in seconds")
#     parser.add_argument("--time", type=str, help='Target time in HH:MM (24hr), e.g. "02:15"')
#     parser.add_argument("--coords", type=str, required=True,
#                         help="List of coordinates, e.g. '[(100,200),(300,400)]'")
#     parser.add_argument("--delay", type=int, default=10, help="Delay between clicks (seconds)")

#     args = parser.parse_args()

#     if not args.seconds and not args.time:
#         print("Provide either --seconds or --time")
#         return

#     try:
#         coordinates = ast.literal_eval(args.coords)
#         if not isinstance(coordinates, list):
#             raise ValueError
#     except:
#         print("Invalid coordinates format. Use: '[(x1,y1),(x2,y2)]'")
#         return

#     # Decide countdown mode
#     if args.time:
#         seconds = seconds_until_target(args.time)
#     else:
#         seconds = args.seconds

#     countdown(seconds, coordinates, args.delay)


# if __name__ == "__main__":
#     main()

# # v02
# import time
# import pyautogui
# import argparse
# import ast
# from datetime import datetime, timedelta

# def show_timer(seconds, message=""):
#     while seconds >= 0:
#         mins, secs = divmod(seconds, 60)
#         timer = f'{mins:02d}:{secs:02d}'
#         print(f"{message}{timer}", end="\r")
#         time.sleep(1)
#         seconds -= 1
#     print()  # move to next line after timer ends


# def countdown(seconds, coordinates, delay_between=10):
#     # Initial countdown
#     print("Starting countdown...")
#     show_timer(seconds, message="Time left: ")

#     print("Time's up! Starting clicks...\n")

#     for i, (x, y) in enumerate(coordinates):
#         pyautogui.click(x, y)
#         print(f"Clicked at ({x}, {y})")

#         # Show timer between clicks (except after last click)
#         if i < len(coordinates) - 1:
#             print(f"Waiting {delay_between} seconds before next click...")
#             show_timer(delay_between, message="Next click in: ")


# def main():
#     parser = argparse.ArgumentParser(description="Countdown clicker script")
#     parser.add_argument("--seconds", type=int, required=True, help="Initial countdown time in seconds")
#     parser.add_argument("--coords", type=str, required=True,
#                         help="List of coordinates, e.g. '[(100,200),(300,400)]'")
#     parser.add_argument("--delay", type=int, default=10, help="Delay between clicks (seconds)")

#     args = parser.parse_args()

#     try:
#         coordinates = ast.literal_eval(args.coords)
#         if not isinstance(coordinates, list):
#             raise ValueError
#     except:
#         print("Invalid coordinates format. Use: '[(x1,y1),(x2,y2)]'")
#         return

#     countdown(args.seconds, coordinates, args.delay)


# if __name__ == "__main__":
#     main()


# v01
# import time
# import pyautogui
# import argparse
# import ast

# def countdown(seconds, coordinates):
#     while seconds >= 0:
#         mins, secs = divmod(seconds, 60)
#         timer = f'{mins:02d}:{secs:02d}'
#         print(timer, end="\r")
#         time.sleep(1)
#         seconds -= 1

#     print("\nTime's up!")

#     for i, (x, y) in enumerate(coordinates):
#         pyautogui.click(x, y)
#         print(f"Clicked at ({x}, {y})")

#         if i < len(coordinates) - 1:
#             time.sleep(10)

# def main():
#     parser = argparse.ArgumentParser(description="Countdown clicker script")
#     parser.add_argument("--seconds", type=int, required=True, help="Countdown time in seconds")
#     parser.add_argument("--coords", type=str, required=True,
#                         help="List of coordinates, e.g. '[(100,200),(300,400)]'")

#     args = parser.parse_args()

#     try:
#         coordinates = ast.literal_eval(args.coords)
#         if not isinstance(coordinates, list):
#             raise ValueError
#     except:
#         print("Invalid coordinates format. Use: '[(x1,y1),(x2,y2)]'")
#         return

#     countdown(args.seconds, coordinates)

# if __name__ == "__main__":
#     main()