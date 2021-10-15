#!/usr/bin/env python
"""
Auto Cookie Clicker by foota, 2013.09.21
ref. http://orteil.dashnet.org/cookieclicker/
"""
import datetime
import json
import logging
import logging.config
import math
import threading
import time
import typing

# import ImageGrab
import pyautogui
# from PIL import Image
from PIL import ImageGrab

DEFAULT_CLICK_PER_SEC = 100
DEFAULT_NUM_CLICK_ONCE = 100
DEFAULT_CLICK_INTERVAL = 1.5
DEFAULT_CHECK_GOLDEN_INTERVAL = 0.5
# X_POS, Y_POS = 70, 351 # pos. of click
# LEFT, RIGHT  = 27, 258 # x-range of browser
# TOP, BOTTOM  = 161, 497 # y-range of browser
WAIT_SEARCH_COOKIE = 3  # WAIT_SEARCH_COOKIE * wait_time (sec)


def distance(t1: typing.Tuple, points: list[typing.Tuple]) -> float:
    """Get color distance."""
    distances = []
    for p in points:
        s = 0
        for i in range(len(t1)):
            s += (p[i] - t1[i]) ** 2
        distances.append(math.sqrt(s))

    return min(distances)


class ClickThread(threading.Thread):
    """Clicker thread."""
    def __init__(self, click_pos_x, click_pos_y, region):
        self.click_pos_x, self.click_pos_y = click_pos_x, click_pos_y
        self.num_clicks_once = DEFAULT_NUM_CLICK_ONCE
        self.wait_time = DEFAULT_CLICK_INTERVAL
        self.is_running = True
        self.watch_cookie_chain = True
        threading.Thread.__init__(self)

        self.region = region
        self.region_x1 = region[0]
        self.region_y1 = region[1]
        self.region_x2 = region[2]
        self.region_y2 = region[3]

        self.width = self.region_x2 - self.region_x1
        self.height = self.region_y2 - self.region_y1

    def check_cookie(self):
        """Check cookie."""
        # im = im.crop((self.region_x1, self.region_y1, self.region_x2, self.region_y2))
        region = (self.region[0], self.region[1], self.width, self.height)
        im = pyautogui.screenshot(region=region)
        cx, cy = -1, -1
        seq = im.convert("RGB").getdata()
        for i, v in enumerate(seq):
            # logging.info("rgb=%d %d %d" % v)
            found = False
            cookie_type = ""
            if distance(v, [(224, 200, 113), (208, 103, 86), (232, 211, 132)]) < 1.05:
                cookie_type = "Golden Cookie"
                found = True
            elif v == (186, 48, 40) or v == (213, 69, 53) or v == (169, 42, 35):
                cookie_type = "Red Cookie"
                found = True

            elif v == (234, 157, 63) or v == (252, 220, 114):
                cookie_type = "Haloween Cookie"
                found = True

            elif v == (184, 120, 76):
                cookie_type = "Wrinkler"
                found = True

            if found:
                cx, cy = int(i % self.width + self.region_x1), int(i / self.width + self.region_y1)
                chained = ""
                if self.watch_cookie_chain:
                    chained = " chained?"
                logging.info("%s%s: (%d, %d) color:(%d %d %d)" % (cookie_type, chained, cx, cy, v[0], v[1], v[2]))
                self.ts_golden_clicked = time.time()
                self.watch_cookie_chain = True
                break

        return (cx, cy)

    def run(self):
        cnt = 0
        error = 0
        click_big_cookie = True
        self.ts_golden_clicked = time.time()
        self.ts_golden_checked = time.time()
        pyautogui.moveTo(self.click_pos_x, self.click_pos_y)

        logging.info("click_pos_x, click_pos_y : (%d, %d)" % (self.click_pos_x, self.click_pos_y))
        while self.is_running:
            cx, cy = -1, -1

            # if (
            #     cur_x < self.region_x1 or self.region_x2 < cur_x
            #     or cur_y < self.region_y1 or self.region_y2 < cur_y
            # ):
            #     logging.info("outside window detected. : (%d, %d)" % (cur_x, cur_y))
            #     break

            time_now = time.time()

            # change interval
            check_golden_interval = DEFAULT_CHECK_GOLDEN_INTERVAL
            if (time_now - self.ts_golden_clicked) < 15:
                # if self.watch_cookie_chain == False:
                #     logging.info("%s: watch cookie chain:" % (str(datetime.datetime.today())))
                self.watch_cookie_chain = True
                check_golden_interval = 0.1
            else:
                # if self.watch_cookie_chain == True:
                #     logging.info("%s: unwatch cookie chain:" % (str(datetime.datetime.today())))
                self.watch_cookie_chain = False
                check_golden_interval = DEFAULT_CHECK_GOLDEN_INTERVAL

            check_golden_flag = False
            if (time_now - self.ts_golden_checked) > check_golden_interval:
                check_golden_flag = True
                self.ts_golden_checked = time_now

            while True:
                (cx, cy) = self.check_cookie()
                if cx < 0 or cy < 0:
                    break
                print("{}: click: {}".format(datetime.datetime.now(), (cx, cy)))
                logging.info("click: (%d, %d)" % (cx, cy))
                pyautogui.click(cx, cy)
                self.ts_golden_clicked = time.time()
                # time.sleep(0.01)

            # try:
            #     if check_golden_flag:
            #         # im = ImageGrab.grab()

            # except Exception:
            #     logging.info("%s: error in SetCursorPos(): (%d, %d)" % (str(datetime.datetime.today()), int(cx), int(cy)))
            #     self.is_running = False
            #     raise

            if click_big_cookie:
                wait_time = 0.2

                # sleeptime_per_click = wait_time / float(DEFAULT_CLICK_PER_SEC)
                loop_num = int(self.num_clicks_once * wait_time)
                pyautogui.moveTo(self.click_pos_x, self.click_pos_y)
                for _ in range(loop_num):
                    p = pyautogui.position()
                    error += math.sqrt((p[0] - self.click_pos_x)**2 + (p[1] - self.click_pos_y)**2)
                    if error > 500:
                        click_big_cookie = False
                        error = 0
                        break
                    pyautogui.click(self.click_pos_x, self.click_pos_y, 1)
                    # time.sleep(sleeptime_per_click)
            else:
                cur_x, cur_y = pyautogui.position()
                if cur_x == 0 and cur_y == 0:
                    break
                d = math.sqrt((cur_x - self.click_pos_x) ** 2 + (cur_y - self.click_pos_y) ** 2)
                if d < 30:
                    click_big_cookie = True

            time.sleep(0.02)
            cnt += 1

    def finish(self):
        self.is_running = False


def clicker(click_pos_x, click_pos_y, region):
    t = ClickThread(click_pos_x, click_pos_y, region)
    # t.setDaemon(True)
    t.start()
    # t.finish()
    t.join()
    while t.is_alive():
        time.sleep(0.5)


def main():
    config = {}
    with open('clicker.json', 'r') as f:
        config = json.load(f)

    click_pos_x = config.get('clickPos')[0]
    click_pos_y = config.get('clickPos')[1]
    region = (
        config.get('region')[0],
        config.get('region')[1],
        config.get('region')[2],
        config.get('region')[3]
    )

    # logging.basicConfig(level = logging.INFO,
    #                    filename='autocookieclicker.log',
    #                    format="%(asctime)s  %(levelname)s: %(message)s",
    #                    datefmt='%Y-%m-%d %I:%M:%S')
    logging.config.fileConfig('clicker.ini')
    logging.getLogger().setLevel(logging.INFO)

    logging.info("POSITION : (%d, %d)" % (click_pos_x, click_pos_y))
    logging.info("AREA     : (%d, %d)-(%d, %d)" % region)

    clicker(click_pos_x, click_pos_y, region)


if __name__ == "__main__":
    main()
