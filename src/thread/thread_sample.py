#!/usr/bin/env python
"""Show thread example."""
import threading
import time
import datetime
# from threading import Thread, Condition


class FooThread(threading.Thread):
    """Define FooThread."""
    def __init__(self):
        self.thread_name = "Foo"
        self.sleep_time = 3
        print("%s:%s init()" % (
            str(datetime.datetime.today()), self.thread_name))
        threading.Thread.__init__(self)

    def run(self):
        print("%s:%s run()#begin" % (
            str(datetime.datetime.today()), self.thread_name))
        time.sleep(self.sleep_time)
        print("%s:%s run()#end" % (
            str(datetime.datetime.today()), self.thread_name))


class BarThread(threading.Thread):
    """Define BarThread."""
    def __init__(self):
        self.thread_name = "Bar"
        self.sleep_time = 2
        print("%s:%s init()" % (
            str(datetime.datetime.today()), self.thread_name))
        threading.Thread.__init__(self)

    def run(self):
        print("%s:%s run()#begin" % (
            str(datetime.datetime.today()), self.thread_name))
        time.sleep(self.sleep_time)
        print("%s:%s run()#end" % (
            str(datetime.datetime.today()), self.thread_name))


def main():
    """Run main."""
    # cv = Condition()
    foo_thread = FooThread()
    bar_thread = BarThread()
    # foo_thread.setDaemon(True)
    # bar_thread.setDaemon(True)
    foo_thread.start()
    bar_thread.start()
    foo_thread.join()
    bar_thread.join()


if __name__ == "__main__":
    main()
