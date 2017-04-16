#!/usr/bin/env python3

from logging import debug
import curses


def logging_level(level, name):
    """Log Level

    Sets the logging level for the app that calls it.

    Args:
        level (str): info, debug, warning
        name (str): name of the app, results in name.log

    Example:
        debug logging for nods::

            logging_level("debug", "nods")

    Returns:
       None
    """
    from logging import basicConfig, getLogger, INFO, DEBUG, WARNING
    from os import makedirs
    from os.path import join, exists

    dataDir = './'
    logDir = join(dataDir, 'log')
    logFile = join(logDir, (name + '.log'))
    exists(logDir) or makedirs(logDir)

    if level == "info":
        basicConfig(
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(message)s',
            filename=logFile,
            level=INFO)
        getLogger("paramiko").setLevel(INFO)
    elif level == "warning":
        basicConfig(
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(message)s',
            filename=logFile,
            level=WARNING)
        getLogger("paramiko").setLevel(WARNING)
    else:
        basicConfig(
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(message)s',
            filename=logFile,
            level=DEBUG)
        getLogger("paramiko").setLevel(DEBUG)


def sketch_setup(stdscr):

    stdscr.addstr("Sketch Pad", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)
    stdscr.addstr(curses.LINES - 1, 0, "Enter Q to quit")
    stdscr.chgat(curses.LINES - 1, 7, 1, curses.A_BOLD | curses.color_pair(2))

    outer_frame = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
    outer_frame.box()
    stdscr.noutrefresh()
    outer_frame.noutrefresh()
    curses.doupdate()


def sketch_print(frame, text):
    frame.refresh()
    frame.clear()
    frame.addstr(text)
    frame.noutrefresh()
    curses.doupdate()


def sketch_error(frame, prompt, err=""):
    if err == "":
        err = "Invalid input please read README.md if you need help"
        sketch_print(frame, "{}{}.".format(prompt, err))
    else:
        sketch_print(frame, "{}Error: {}.".format(prompt, err))
    frame.getch()
    sketch_print(frame, prompt)


class Pad(object):
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h
        self.max_w = curses.COLS - 4
        self.max_h = curses.LINES - 6

    def new(self):
        if self.w > self.max_w or self.h > self.max_h or self.w < 2 or self.h < 2:
            return "Illegal pad size, pad must be between w:2-{} h:2-{}".format(
                self.max_w, self.max_h)
        self.frame = curses.newwin(self.h, self.w, 4, 2)
        self.frame.box()
        self.frame.noutrefresh()
        curses.doupdate()
        return None

    def used(self):
        if self.w == 0 or self.h == 0:
            return False
        else:
            return True

    def frame(self):
        return self.frame


def sketch_input():
    prompt = "Enter command: "
    input_frame = curses.newwin(1, curses.COLS - 4, 3, 2)
    curses.echo()
    sketch_print(input_frame, prompt)
    pad = Pad()
    while True:
        c = input_frame.getstr()
        debug(c)
        if len(c) > 1:
            cmd = c.decode("utf8").split()
            debug(cmd)
            if cmd[0].lower() == 'c' and len(cmd) == 3:
                if pad.used():
                    sketch_error(
                        input_frame, prompt,
                        "Pad already created, get drawing or quit to start again"
                    )
                else:
                    try:
                        w = int(cmd[1])
                        h = int(cmd[2])
                        sketch_print(input_frame, prompt)
                        pad = Pad(w, h)
                        err = pad.new()
                        if err != None:
                            sketch_error(input_frame, prompt, err)
                    except Exception as err:
                        sketch_error(input_frame, prompt, str(err))
            elif cmd[0].lower() == 'l' and len(cmd) == 5:
                pass
            else:
                sketch_error(input_frame, prompt)
        elif c == b'':
            sketch_print(input_frame, prompt)
        elif c == b'q' or c == b'Q':
            break
        else:
            sketch_error(input_frame, prompt)

        curses.doupdate()
    curses.noecho()


def main(stdscr):
    logging_level('debug', 'sketch')
    sketch_setup(stdscr)
    sketch_input()


if __name__ == "__main__":
    curses.wrapper(main)
