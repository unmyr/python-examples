"""Example of a pyautogui."""
import math

import pyautogui


def main():
    """Run main."""
    error = 0
    tx, ty = 159, 435
    pyautogui.moveTo(tx, ty)
    for _ in range(10000):
        p = pyautogui.position()
        error += math.sqrt((p[0] - tx) ** 2 + (p[1] - ty) ** 2)
        if error > 1000:
            break
        pyautogui.click(tx, ty)


if __name__ == "__main__":
    main()

# EOF
