import time
import pyautogui
import argparse
import ast

def countdown(seconds, coordinates):
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1

    print("\nTime's up!")

    for i, (x, y) in enumerate(coordinates):
        pyautogui.click(x, y)
        print(f"Clicked at ({x}, {y})")

        if i < len(coordinates) - 1:
            time.sleep(10)

def main():
    parser = argparse.ArgumentParser(description="Countdown clicker script")
    parser.add_argument("--seconds", type=int, required=True, help="Countdown time in seconds")
    parser.add_argument("--coords", type=str, required=True,
                        help="List of coordinates, e.g. '[(100,200),(300,400)]'")

    args = parser.parse_args()

    try:
        coordinates = ast.literal_eval(args.coords)
        if not isinstance(coordinates, list):
            raise ValueError
    except:
        print("Invalid coordinates format. Use: '[(x1,y1),(x2,y2)]'")
        return

    countdown(args.seconds, coordinates)

if __name__ == "__main__":
    main()