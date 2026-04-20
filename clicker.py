# v03

import time
import pyautogui
import argparse
import ast
from datetime import datetime, timedelta


def show_timer(seconds, message=""):
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f"{message}{timer}", end="\r")
        time.sleep(1)
        seconds -= 1
    print()


def seconds_until_target(time_str):
    now = datetime.now()

    # Parse HH:MM (24-hour format)
    target = datetime.strptime(time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )

    # If already passed today → move to tomorrow
    if target <= now:
        target += timedelta(days=1)

    return int((target - now).total_seconds())


def countdown(seconds, coordinates, delay_between=10):
    print("Starting countdown...")
    show_timer(seconds, message="Time left: ")

    print("Time's up! Starting clicks...\n")

    for i, (x, y) in enumerate(coordinates):
        pyautogui.click(x, y)
        print(f"Clicked at ({x}, {y})")

        if i < len(coordinates) - 1:
            print(f"Waiting {delay_between} seconds before next click...")
            show_timer(delay_between, message="Next click in: ")


def main():
    parser = argparse.ArgumentParser(description="Countdown clicker script")

    parser.add_argument("--seconds", type=int, help="Countdown time in seconds")
    parser.add_argument("--time", type=str, help='Target time in HH:MM (24hr), e.g. "02:15"')
    parser.add_argument("--coords", type=str, required=True,
                        help="List of coordinates, e.g. '[(100,200),(300,400)]'")
    parser.add_argument("--delay", type=int, default=10, help="Delay between clicks (seconds)")

    args = parser.parse_args()

    if not args.seconds and not args.time:
        print("Provide either --seconds or --time")
        return

    try:
        coordinates = ast.literal_eval(args.coords)
        if not isinstance(coordinates, list):
            raise ValueError
    except:
        print("Invalid coordinates format. Use: '[(x1,y1),(x2,y2)]'")
        return

    # Decide countdown mode
    if args.time:
        seconds = seconds_until_target(args.time)
    else:
        seconds = args.seconds

    countdown(seconds, coordinates, args.delay)


if __name__ == "__main__":
    main()

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